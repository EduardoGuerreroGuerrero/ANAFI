import logging

logger = logging.getLogger(__name__)


def calculate_breakeven_point(
    costos_fijos_mensuales: float,
    costo_variable_unitario: float,
    precio_venta_unitario: float,
    volumen_ventas_estimado: int,
) -> str:
    """
    Calcula el punto de equilibrio en unidades y en dinero.
    
    Args:
        costos_fijos_mensuales: Costos fijos mensuales del negocio
        costo_variable_unitario: Costo variable por unidad
        precio_venta_unitario: Precio de venta por unidad
        volumen_ventas_estimado: Volumen de ventas estimado mensual
    
    Fórmulas:
    - Punto de Equilibrio (unidades) = Costos Fijos / (Precio de Venta - Costo Variable Unitario)
    - Punto de Equilibrio (dinero) = Punto de Equilibrio (unidades) × Precio de Venta
    """
    try:
        # Calcular margen de contribución unitario
        margen_contribucion = precio_venta_unitario - costo_variable_unitario
        
        if margen_contribucion <= 0:
            return "❌ Error: El precio de venta debe ser mayor que el costo variable unitario."
        
        # Calcular punto de equilibrio
        pe_unidades = costos_fijos_mensuales / margen_contribucion
        pe_dinero = pe_unidades * precio_venta_unitario
        
        # Verificar alerta
        alerta = ""
        if pe_unidades > volumen_ventas_estimado:
            alerta = f"\n\n⚠️ ALERTA CRÍTICA: El punto de equilibrio ({pe_unidades:.0f} unidades) es MAYOR que las ventas proyectadas ({volumen_ventas_estimado} unidades). El negocio NO sería viable con estos parámetros."
        
        message = f"""✅ Punto de equilibrio calculado:
- En unidades: {pe_unidades:.2f} unidades/mes
- En dinero: ${pe_dinero:,.2f}/mes{alerta}"""
        
        logger.info(f"Punto de equilibrio: {pe_unidades:.2f} unidades, ${pe_dinero:,.2f}")
        
        return message
        
    except Exception as e:
        logger.error(f"Error calculando punto de equilibrio: {str(e)}")
        return f"❌ Error al calcular punto de equilibrio: {str(e)}"
