from pydantic import BaseModel
from typing import List


class Alert(BaseModel):
    """Alerta generada por el sistema."""
    tipo: str  # "critica", "advertencia", "informacion"
    mensaje: str
    

class FinancialReport(BaseModel):
    """Reporte financiero completo."""
    nombre_negocio: str
    fecha_generacion: str
    metricas_basicas: dict
    analisis_avanzado: dict
    escenarios: List[dict]
    alertas: List[Alert]
