import logging

logger = logging.getLogger(__name__)


def calculate_profitability_ratios(
    precio_venta_unitario: float,
    costo_variable_unitario: float,
    costos_fijos_mensuales: float,
    volumen_ventas_estimado: int,
    inversion_inicial: float = None,
) -> str:
    """
    Calcula los ratios de rentabilidad (ROS y ROI).
    
    Args:
        precio_venta_unitario: Precio de venta por unidad
        costo_variable_unitario: Costo variable por unidad
        costos_fijos_mensuales: Costos fijos mensuales
        volumen_ventas_estimado: Volumen de ventas estimado
        inversion_inicial: Inversión inicial (opcional)
    
    Fórmulas:
    - ROS (Rentabilidad sobre Ventas) = (Utilidad Neta / Ventas Totales) × 100
    - ROI (Rentabilidad sobre Inversión) = (Utilidad Neta / Inversión Inicial) × 100
    """
    try:
        # Calcular ventas y utilidad
        ventas_totales = precio_venta_unitario * volumen_ventas_estimado
        costos_variables_totales = costo_variable_unitario * volumen_ventas_estimado
        costos_totales = costos_fijos_mensuales + costos_variables_totales
        utilidad_neta = ventas_totales - costos_totales
        
        # Calcular ROS
        ros = (utilidad_neta / ventas_totales) * 100 if ventas_totales > 0 else 0
        
        # Calcular ROI (si hay inversión inicial)
        roi_anual = None
        if inversion_inicial and inversion_inicial > 0:
            utilidad_neta_anual = utilidad_neta * 12  # Anualizar
            roi_anual = (utilidad_neta_anual / inversion_inicial) * 100
        
        # Verificar alertas
        alerta = ""
        if ros < 10:
            alerta = "\n\n⚠️ ADVERTENCIA: La rentabilidad sobre ventas (ROS) es menor al 10%. Considera optimizar costos."
        if roi_anual and roi_anual < 15:
            alerta += "\n⚠️ ADVERTENCIA: El ROI anual es menor al 15%. La inversión podría no ser atractiva."
        
        roi_msg = f"\n- ROI anual: {roi_anual:.2f}%" if roi_anual else ""
        
        message = f"""✅ Rentabilidad calculada:
- ROS (Rentabilidad sobre Ventas): {ros:.2f}%{roi_msg}{alerta}"""
        
        logger.info(f"ROS: {ros:.2f}%, ROI: {roi_anual}")
        
        return message
        
    except Exception as e:
        logger.error(f"Error calculando rentabilidad: {str(e)}")
        return f"❌ Error al calcular rentabilidad: {str(e)}"
