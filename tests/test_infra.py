"""Pruebas de la infraestructura: sintetizan el stack sin desplegarlo."""

import aws_cdk as cdk
import pytest
from aws_cdk.assertions import Match, Template

from infra.stacks.frescura_stack import FrescuraStack, modelo_base


@pytest.fixture(scope="module")
def plantilla():
    app = cdk.App()
    stack = FrescuraStack(app, "Frescura-prueba", participante="prueba", modelo_vision="us.amazon.nova-2-lite-v1:0")
    return Template.from_stack(stack)


def test_modelo_base_quita_el_prefijo_geografico():
    assert modelo_base("us.amazon.nova-2-lite-v1:0") == "amazon.nova-2-lite-v1:0"
    assert modelo_base("amazon.nova-2-lite-v1:0") == "amazon.nova-2-lite-v1:0"


def test_la_funcion_solo_puede_invocar_el_modelo_configurado(plantilla):
    plantilla.has_resource_properties(
        "AWS::IAM::Policy",
        {
            "PolicyDocument": {
                "Statement": Match.array_with(
                    [
                        Match.object_like(
                            {
                                "Action": "bedrock:InvokeModel",
                                "Resource": Match.array_with(
                                    ["arn:aws:bedrock:*::foundation-model/amazon.nova-2-lite-v1:0"]
                                ),
                            }
                        )
                    ]
                )
            }
        },
    )


def test_la_funcion_solo_escribe_en_el_historial(plantilla):
    plantilla.has_resource_properties(
        "AWS::IAM::Policy",
        {
            "PolicyDocument": {
                "Statement": Match.array_with([Match.object_like({"Action": "dynamodb:PutItem", "Effect": "Allow"})])
            }
        },
    )


def test_la_api_tiene_limite_de_uso(plantilla):
    plantilla.has_resource_properties(
        "AWS::ApiGatewayV2::Stage",
        {"DefaultRouteSettings": {"ThrottlingBurstLimit": 10, "ThrottlingRateLimit": 5}},
    )


def test_el_bucket_de_la_web_no_es_publico(plantilla):
    plantilla.has_resource_properties(
        "AWS::S3::Bucket",
        {
            "PublicAccessBlockConfiguration": {
                "BlockPublicAcls": True,
                "BlockPublicPolicy": True,
                "IgnorePublicAcls": True,
                "RestrictPublicBuckets": True,
            }
        },
    )


def test_publica_la_vista_del_personal_y_la_del_cliente(plantilla):
    salidas = plantilla.find_outputs("*")
    assert {"UrlWeb", "UrlCliente"} <= salidas.keys()
