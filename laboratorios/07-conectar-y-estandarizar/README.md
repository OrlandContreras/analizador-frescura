# Lab 7 · Conectar y estandarizar

**Módulo 7 · L300 · 20 minutos · Rama de inicio: `lab-07`**

## Qué vas a hacer

Vas a darle al agente dos capacidades nuevas:

- **MCP (Model Context Protocol):** conecta al agente con herramientas externas. Aquí, dos servidores oficiales de AWS: uno para consultar la **documentación** y otro para consultar **precios reales**.
- **Skills:** procedimientos del equipo empaquetados para reutilizar. Aquí, uno que arma la **ficha de un producto** y otro que **estima el costo del piloto** usando los precios de AWS.

Con eso, al final del laboratorio tendrás una estimación de cuánto costaría llevar el analizador a 5 tiendas, con precios consultados y no inventados.

## Objetivo

Consultar documentación y precios de AWS desde Kiro, y usar dos skills reutilizables que producen entregables del proyecto.

## Antes de empezar

- **Sigues con tu trabajo:** quédate en tu rama.
- **Te atrasaste:**

```bash
git stash --include-untracked
git switch lab-07
pip install -r requirements-dev.txt
```

Comprueba que `uv --version` y `aws sts get-caller-identity` funcionan en la terminal.

## Paso a paso

### Paso 1. Trae la configuración de MCP y las skills

```bash
git restore --source lab-08 -- .kiro/settings/mcp.json .kiro/skills
```

> Si clonaste el proyecto de GitHub y no encuentra `lab-08`, usa `origin/lab-08`.

### Paso 2. Revisa la configuración de MCP

Abre `.kiro/settings/mcp.json`. Tiene dos servidores:

- `aws-docs`: documentación oficial de AWS. No necesita credenciales.
- `aws-pricing`: precios de AWS. Usa tu perfil de AWS (`AWS_PROFILE`).

Si tu perfil de AWS no se llama `default`, cambia `"AWS_PROFILE": "default"` por el nombre de tu perfil y guarda.

En **Windows**, cambia en cada servidor `"command": "uvx"` y sus `args` por esta forma (el ejemplo es para `aws-docs`; para precios cambia el nombre del paquete):

```json
"command": "uv",
"args": ["tool", "run", "--from", "awslabs.aws-documentation-mcp-server@latest", "awslabs.aws-documentation-mcp-server.exe"]
```

### Paso 3. Comprueba que se conectaron

En el panel de Kiro, sección **MCP SERVERS**, deben aparecer `aws-docs` y `aws-pricing` como **Connected**. La primera vez tardan hasta un minuto en descargarse.

### Paso 4. Consulta la documentación de AWS

En una conversación nueva (**+**):

```text
Usando la documentación oficial de AWS, ¿cuál es el tamaño máximo del cuerpo de una invocación síncrona de AWS Lambda? Relaciónalo con el límite de 4 MB que valida app/frescura/handler.py y con que la web reduzca la foto a 1024 px.
```

**Resultado esperado:** Kiro usa el servidor `aws-docs` (lo ves en las herramientas que llama) y responde que el límite de la carga útil síncrona es de **6 MB**, citando la página de AWS. Explica que la imagen en base64 crece cerca de un tercio, por eso el handler limita a 4 MB y la web reduce la foto.

### Paso 5. Usa la skill de ficha de producto

Abre `.kiro/skills/ficha-producto/SKILL.md` y lee qué fuentes debe usar. Luego, en el chat:

```text
Dame la ficha del mango.
```

**Resultado esperado:** Kiro activa la skill `ficha-producto` y arma la ficha con los datos del proyecto: umbrales 25, 55 y 85; 10 puntos por día; **6 días** desde verde hasta su punto; destino "jugos o pulpa"; 60 kcal, 1,6 g de fibra, 168 mg de potasio y 36,4 mg de vitamina C por 100 g; y un mensaje para el cliente sin promesas de salud.

### Paso 6. Estima el costo del piloto

```text
Estima el costo mensual del piloto con 5 tiendas y 200 fotos por tienda al día.
```

**Resultado esperado:** Kiro activa la skill `estimar-costo-piloto`, consulta precios con el servidor `aws-pricing` y crea `docs/costo-piloto.md` con la tabla de supuestos, el costo por servicio con su fórmula, el total mensual y el costo por foto. Abre el archivo y revisa qué servicio domina el costo.

### Paso 7. Guarda tu trabajo

```bash
git add -A
git commit -m "Lab 7: MCP de AWS, skills y estimación de costo"
```

## Criterio de éxito

- [ ] `aws-docs` y `aws-pricing` aparecen como **Connected**.
- [ ] La respuesta sobre Lambda cita la documentación de AWS.
- [ ] La ficha del mango usa los datos del proyecto.
- [ ] Existe `docs/costo-piloto.md` con precios consultados.

## Si algo no sale

| Síntoma | Qué hacer |
| --- | --- |
| Un servidor no conecta | Revisa `uv --version`. Luego mira los registros: menú **View → Output** y elige **Kiro - MCP Logs** |
| `aws-pricing` da error de permisos | Tu usuario necesita permiso `pricing:*`. Avisa al equipo de AWS |
| Kiro no activa la skill | Escríbela con `/`: `/ficha-producto mango` |
| La estimación usa precios "de memoria" | Escribe: "Consulta cada precio con el servidor aws-pricing y cita la consulta" |
| Te quedaste sin tiempo | Cambia a la rama `lab-08` |
