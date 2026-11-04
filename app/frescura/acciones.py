"""Acción recomendada en tienda según la política POL-FRV-001 (negocio/politica-acciones-tienda.md).

Las reglas se evalúan en orden: la primera que se cumple decide la acción.
"""

from __future__ import annotations

from .vision import LecturaVision

UMBRAL_CONFIANZA = 0.70
MANCHAS_TRANSFORMAR = 30
MANCHAS_DONAR = 60


def recomendar_accion(lectura: LecturaVision, etapa: str | None, producto: dict | None) -> dict:
    """Devuelve {"tipo", "mensaje", "requiere_confirmacion"} para el personal de la sección."""
    if producto is None or etapa is None or lectura.confianza < UMBRAL_CONFIANZA:
        return _accion("revisar", "Revisar el producto: el análisis no es concluyente", confirmar=True)
    if "moho" in lectura.defectos:
        return _accion("retirar", "Retirar y descartar: el producto tiene moho")
    if etapa in ("verde", "pinton"):
        return _accion("mantener", "Mantener en góndola a precio normal")
    if etapa == "maduro":
        return _accion("priorizar", "Exhibir al frente para que se venda primero")
    if lectura.manchas_pct >= MANCHAS_DONAR:
        return _accion("donar", "Retirar y entregar hoy al banco de alimentos", confirmar=True)
    if lectura.manchas_pct >= MANCHAS_TRANSFORMAR or "zonas_hundidas" in lectura.defectos:
        return _accion("transformar", f"Enviar a {producto['transformacion']}")
    return _accion("rebajar", "Rebajar 30% y etiquetar como consumo inmediato")


def _accion(tipo: str, mensaje: str, confirmar: bool = False) -> dict:
    return {"tipo": tipo, "mensaje": mensaje, "requiere_confirmacion": confirmar}
