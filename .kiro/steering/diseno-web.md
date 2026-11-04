---
inclusion: fileMatch
fileMatchPattern: "web/**"
---

# Guía visual de la página web

La página la usa el personal de tienda desde el celular, con una mano y a veces con poca luz. El diseño es de alto contraste, directo y amable.

## Colores

Usa siempre las variables de `:root` en `web/index.html`. No escribas colores sueltos en el HTML ni en el JavaScript.

| Variable | Valor | Uso |
| --- | --- | --- |
| `--marca` | `#ffe100` (amarillo) | Franja del encabezado, resaltados y anillo de foco |
| `--marca-texto` | `#1a1a1a` | Texto sobre amarillo. Nunca pongas texto blanco sobre amarillo |
| `--marca-suave` | `#fff6bf` | Fondo de los mensajes destacados, como el mensaje para el cliente |
| `--acento` / `--acento-texto` | negro con texto amarillo (en modo oscuro, al revés) | Botón principal |
| `--verde`, `--pinton`, `--maduro`, `--sobremaduro` | Colores de las etapas | Solo para la etiqueta de la etapa |

El modo oscuro se define en el bloque `@media (prefers-color-scheme: dark)`. Todo color nuevo necesita su valor en los dos modos.

## Tipografía y formas

- Letra del sistema (`system-ui`). Títulos en peso 800; etiquetas y valores en 700.
- Tarjetas con bordes redondeados de 18 px (`--radio`); botones en forma de píldora (`border-radius: 999px`).
- Un solo botón principal por pantalla.

## Reglas

- **No uses logotipos, imágenes ni nombres de empresas o marcas reales.** El producto se llama "Analizador de frescura".
- Contraste mínimo 4,5:1 entre texto y fondo. El amarillo solo va con texto oscuro.
- La página debe verse bien a 360 px de ancho, sin desplazamiento horizontal.
- Todo texto visible va en español y en tuteo, siguiendo `mensajes-cliente.md`.
