import json
import logging
from src.models.financial_data import BusinessInputData

logger = logging.getLogger(__name__)


def save_business_data(data: dict) -> str:
    """Valida y formatea los datos del negocio.
    
    Args:
        data: Diccionario con los datos del negocio
        
    Returns:
        Mensaje de confirmación con resumen de los datos validados
    """
    
    try:
        # Validar con Pydantic
        business_data = BusinessInputData(**data)
        
        logger.info(f"Datos validados: {business_data.nombre_negocio}")
        
        return f"""✅ Datos validados exitosamente

Resumen de datos:
- Negocio: {business_data.nombre_negocio} ({business_data.tipo_negocio})
- Costos fijos mensuales: ${business_data.costos_fijos_mensuales:,.2f}
- Costo variable unitario: ${business_data.costo_variable_unitario:,.2f}
- Precio de venta unitario: ${business_data.precio_venta_unitario:,.2f}
- Volumen estimado: {business_data.volumen_ventas_estimado} unidades/mes
{f'- Inversión inicial: ${business_data.inversion_inicial:,.2f}' if business_data.inversion_inicial else ''}

Datos JSON:
{json.dumps(business_data.model_dump(), indent=2, ensure_ascii=False)}
"""
        
    except Exception as e:
        logger.error(f"Error al validar datos: {str(e)}")
        return f"❌ Error al validar datos: {str(e)}"
