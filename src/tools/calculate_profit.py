import logging

logger = logging.getLogger(__name__)


def calculate_profit(
    precio_venta_unitario: float,
    costo_variable_unitario: float,
    costos_fijos_mensuales: float,
    volumen_ventas_estimado: int,
) -> str:
    """
    Calcula la utilidad bruta y neta del negocio.
    
    Args:
        precio_venta_unitario: Precio de venta por unidad
        costo_variable_unitario: Costo variable por unidad
        costos_fijos_mensuales: Costos fijos mensuales
        volumen_ventas_estimado: Volumen de ventas estimado
    
    Fórmulas:
    - Ventas Totales = Precio de Venta × Volumen de Ventas
    - Costos Variables Totales = Costo Variable Unitario × Volumen de Ventas
    - Utilidad Bruta = Ventas Totales - Costos Variables Totales
    - Utilidad Neta = Ventas Totales - Costos Totales
    """
    try:
        # Calcular ventas totales
        ventas_totales = precio_venta_unitario * volumen_ventas_estimado
        
        # Calcular costos
        costos_variables_totales = costo_variable_unitario * volumen_ventas_estimado
        costos_totales = costos_fijos_mensuales + costos_variables_totales
        
        # Calcular utilidades
        utilidad_bruta = ventas_totales - costos_variables_totales
        utilidad_neta = ventas_totales - costos_totales
        
        # Verificar alertas
        alerta = ""
        if utilidad_neta < 0:
            alerta = "\n\n⚠️ ALERTA: El negocio está generando PÉRDIDAS. La utilidad neta es negativa."
        elif utilidad_neta < (ventas_totales * 0.10):
            alerta = "\n\n⚠️ ADVERTENCIA: La utilidad neta es menor al 10% de las ventas. Considera optimizar costos o aumentar precios."
        
        message = f"""✅ Utilidades calculadas:
- Ventas totales: ${ventas_totales:,.2f}/mes
- Utilidad bruta: ${utilidad_bruta:,.2f}/mes
- Utilidad neta: ${utilidad_neta:,.2f}/mes{alerta}"""
        
        logger.info(f"Utilidad neta: ${utilidad_neta:,.2f}")
        
        return message
        
    except Exception as e:
        logger.error(f"Error calculando utilidad: {str(e)}")
        return f"❌ Error al calcular utilidad: {str(e)}"
