from pydantic import BaseModel, Field
from typing import Optional, List, Literal


class BusinessInputData(BaseModel):
    """Datos de entrada del negocio proporcionados por el usuario."""
    nombre_negocio: str = Field(description="Nombre del negocio")
    tipo_negocio: str = Field(description="Tipo de negocio (ej: cafetería, tienda)")
    costos_fijos_mensuales: float = Field(gt=0, description="Costos fijos mensuales")
    costo_variable_unitario: float = Field(ge=0, description="Costo variable por unidad")
    precio_venta_unitario: float = Field(gt=0, description="Precio de venta por unidad")
    volumen_ventas_estimado: int = Field(gt=0, description="Volumen de ventas estimado")
    inversion_inicial: Optional[float] = Field(None, ge=0, description="Inversión inicial (opcional)")


class BasicMetrics(BaseModel):
    """Métricas financieras básicas calculadas."""
    costos_totales: float
    punto_equilibrio_unidades: float
    punto_equilibrio_dinero: float
    utilidad_bruta: float
    utilidad_neta: float
    rentabilidad_sobre_ventas: float  # ROS en porcentaje
    rentabilidad_sobre_inversion: Optional[float] = None  # ROI en porcentaje


class MonthlyFlow(BaseModel):
    """Flujo de efectivo de un mes específico."""
    mes: int
    entradas: float
    salidas: float
    flujo_neto: float
    saldo_acumulado: float


class CashflowProjection(BaseModel):
    """Proyección de flujo de efectivo."""
    proyeccion_meses: int
    flujos_mensuales: List[MonthlyFlow]
    alertas: List[str] = []


class ScenarioData(BaseModel):
    """Datos de un escenario financiero."""
    nombre_escenario: str
    tipo: Literal["pesimista", "moderado", "optimista", "personalizado"]
    precio_venta: float
    costo_variable: float
    volumen_ventas: int
    costos_fijos: float
    metricas_calculadas: BasicMetrics
