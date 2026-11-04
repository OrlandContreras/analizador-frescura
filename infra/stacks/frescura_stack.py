"""Infraestructura del analizador: API, función, historial y página web de captura."""

from pathlib import Path

from aws_cdk import CfnOutput, Duration, RemovalPolicy, Stack
from aws_cdk import aws_apigatewayv2 as apigw
from aws_cdk import aws_apigatewayv2_integrations as integraciones
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_cloudfront_origins as origenes
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_logs as logs
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3deploy
from constructs import Construct

RAIZ = Path(__file__).resolve().parents[2]


def modelo_base(perfil: str) -> str:
    """Quita el prefijo geográfico de un perfil de inferencia (us., eu., global.)."""
    partes = perfil.split(".", 1)
    if len(partes) == 2 and partes[0] in {"us", "eu", "apac", "ca", "jp", "global"}:
        return partes[1]
    return perfil


class FrescuraStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, *, participante: str, modelo_vision: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Historial de análisis (sin imágenes). Se borra con el stack: es un entorno de taller.
        tabla = dynamodb.Table(
            self,
            "Analisis",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )

        registros = logs.LogGroup(
            self,
            "Registros",
            retention=logs.RetentionDays.ONE_WEEK,
            removal_policy=RemovalPolicy.DESTROY,
        )

        funcion = lambda_.Function(
            self,
            "Analizador",
            runtime=lambda_.Runtime.PYTHON_3_12,
            architecture=lambda_.Architecture.ARM_64,
            handler="frescura.handler.lambda_handler",
            code=lambda_.Code.from_asset(str(RAIZ / "app"), exclude=["**/__pycache__", "**/AGENTS.md"]),
            timeout=Duration.seconds(30),
            memory_size=512,
            environment={"TABLA_ANALISIS": tabla.table_name, "MODELO_VISION": modelo_vision},
            log_group=registros,
        )
        tabla.grant(funcion, "dynamodb:PutItem")

        # Solo el modelo de visión configurado: el perfil de inferencia y el modelo base en sus regiones.
        funcion.add_to_role_policy(
            iam.PolicyStatement(
                actions=["bedrock:InvokeModel"],
                resources=[
                    f"arn:aws:bedrock:{self.region}:{self.account}:inference-profile/{modelo_vision}",
                    f"arn:aws:bedrock:*::foundation-model/{modelo_base(modelo_vision)}",
                ],
            )
        )

        api = apigw.HttpApi(
            self,
            "Api",
            api_name=f"frescura-{participante}",
            cors_preflight=apigw.CorsPreflightOptions(
                allow_origins=["*"],
                allow_methods=[apigw.CorsHttpMethod.GET, apigw.CorsHttpMethod.POST],
                allow_headers=["content-type"],
            ),
        )
        integracion = integraciones.HttpLambdaIntegration("Integracion", funcion)
        api.add_routes(path="/salud", methods=[apigw.HttpMethod.GET], integration=integracion)
        api.add_routes(path="/productos", methods=[apigw.HttpMethod.GET], integration=integracion)
        api.add_routes(path="/analisis", methods=[apigw.HttpMethod.POST], integration=integracion)

        # Límite de uso para un entorno de taller: protege el costo de Bedrock.
        etapa = api.default_stage.node.default_child
        etapa.add_property_override("DefaultRouteSettings.ThrottlingBurstLimit", 10)
        etapa.add_property_override("DefaultRouteSettings.ThrottlingRateLimit", 5)

        # Página web de captura: bucket privado servido por CloudFront.
        sitio = s3.Bucket(
            self,
            "Sitio",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            enforce_ssl=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )
        distribucion = cloudfront.Distribution(
            self,
            "Web",
            default_root_object="index.html",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origenes.S3BucketOrigin.with_origin_access_control(sitio),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
        )
        s3deploy.BucketDeployment(
            self,
            "PublicarWeb",
            destination_bucket=sitio,
            distribution=distribucion,
            sources=[
                s3deploy.Source.asset(str(RAIZ / "web")),
                s3deploy.Source.json_data("config.json", {"api": api.api_endpoint, "participante": participante}),
            ],
        )

        CfnOutput(self, "UrlApi", value=api.api_endpoint)
        CfnOutput(self, "UrlWeb", value=f"https://{distribucion.distribution_domain_name}")
        CfnOutput(self, "UrlCliente", value=f"https://{distribucion.distribution_domain_name}/cliente.html")
        CfnOutput(self, "TablaAnalisis", value=tabla.table_name)
        CfnOutput(self, "GrupoRegistros", value=registros.log_group_name)
