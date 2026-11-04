"""Mensaje para el cliente final, según .kiro/steering/mensajes-cliente.md.

Tuteo, máximo dos frases, sin promesas de salud y con el día en que el producto
estará en su punto.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

# Colombia no tiene horario de verano: UTC-5 todo el año.
ZONA_COLOMBIA = timezone(timedelta(hours=-5))
DIAS_SEMANA = ("lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo")


def hoy_en_colombia() -> date:
    return datetime.now(ZONA_COLOMBIA).date()


def mensaje_cliente(nombre: str | None, etapa: str | None, dias: int | None, hoy: date | None = None) -> str | None:
    """Devuelve el mensaje para el cliente, o None si el producto no se reconoció."""
    if not nombre or etapa is None or dias is None:
        return None
    producto = nombre.lower()
    if etapa == "sobremaduro":
        return f"Tu {producto} ya pasó su mejor punto. Aprovéchalo hoy en jugos, batidos o preparaciones."
    if etapa == "maduro" or dias == 0:
        return f"Tu {producto} está en su punto. Disfrútalo hoy o mañana."
    if dias == 1:
        return f"Tu {producto} estará en su punto mañana. Mientras tanto, déjalo a temperatura ambiente."
    dia = DIAS_SEMANA[((hoy or hoy_en_colombia()) + timedelta(days=dias)).weekday()]
    return f"Tu {producto} estará en su punto el {dia}. Mientras tanto, déjalo a temperatura ambiente."
