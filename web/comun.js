// Funciones compartidas por la vista del personal (index.html) y la del cliente (cliente.html).

const LADO_MAXIMO = 1024;
let config = null;

async function cargarConfig() {
  const r = await fetch("config.json", { cache: "no-store" });
  config = await r.json();
  document.getElementById("participante").textContent = "Instancia: " + config.participante;
}

function reducirImagen(archivo) {
  return new Promise((resolver, rechazar) => {
    const img = new Image();
    img.onload = () => {
      const escala = Math.min(1, LADO_MAXIMO / Math.max(img.width, img.height));
      const lienzo = document.createElement("canvas");
      lienzo.width = Math.round(img.width * escala);
      lienzo.height = Math.round(img.height * escala);
      lienzo.getContext("2d").drawImage(img, 0, 0, lienzo.width, lienzo.height);
      resolver(lienzo.toDataURL("image/jpeg", 0.85));
      URL.revokeObjectURL(img.src);
    };
    img.onerror = () => rechazar(new Error("No se pudo leer la imagen"));
    img.src = URL.createObjectURL(archivo);
  });
}

const NOMBRES_ETAPA = { verde: "Verde", pinton: "Pintón", maduro: "Maduro", sobremaduro: "Sobremaduro" };

// Muestra las fotos de muestra (web/muestras) y llama a analizar(blob, muestra) al tocar una.
async function cargarMuestras(analizar) {
  const r = await fetch("muestras/muestras.json", { cache: "no-store" });
  if (!r.ok) return;
  const { muestras } = await r.json();
  const caja = document.getElementById("muestras");
  for (const m of muestras) {
    const b = document.createElement("button");
    b.type = "button"; b.className = "muestra"; b.title = m.titulo; b.setAttribute("aria-label", "Analizar " + m.titulo);
    const img = document.createElement("img");
    img.src = "muestras/" + m.archivo; img.alt = ""; img.loading = "lazy";
    b.append(img);
    b.addEventListener("click", async () => {
      const foto = await fetch("muestras/" + m.archivo);
      await analizar(await foto.blob(), m);
    });
    caja.append(b);
  }
  document.getElementById("caja-muestras").hidden = false;
}
