import logging

logger = logging.getLogger(__name__)


def calculate_total_costs(
    costos_fijos_mensuales: float,
    costo_variable_unitario: float,
    volumen_ventas_estimado: int,
) -> str:
    """
    Calcula los costos totales del negocio.
    
    Args:
        costos_fijos_mensuales: Costos fijos mensuales
        costo_variable_unitario: Costo variable por unidad
        volumen_ventas_estimado: Volumen de ventas estimado
    
    Fórmula:
    Costos Totales = Costos Fijos + (Costo Variable Unitario × Volumen de Ventas)
    """
    try:
        # Calcular costos variables totales
        costos_variables_totales = costo_variable_unitario * volumen_ventas_estimado
        
        # Calcular costos totales
        costos_totales = costos_fijos_mensuales + costos_variables_totales
        
        message = f"""✅ Costos calculados:
- Costos fijos: ${costos_fijos_mensuales:,.2f}/mes
- Costos variables totales: ${costos_variables_totales:,.2f}/mes
- Costos totales: ${costos_totales:,.2f}/mes"""
        
        logger.info(f"Costos totales: ${costos_totales:,.2f}")
        
        return message
        
    except Exception as e:
        logger.error(f"Error calculando costos: {str(e)}")
        return f"❌ Error al calcular costos: {str(e)}"
