import logging
from typing import Any

logger = logging.getLogger(__name__)


def validate_financial_data(
    field_name: str,
    value: Any,
    costo_variable_unitario: float = None,
) -> str:
    """Valida que un campo financiero sea válido.
    
    Args:
        field_name: Nombre del campo a validar
        value: Valor a validar
        costo_variable_unitario: Costo variable unitario (opcional, para validar precio de venta)
    """
    
    try:
        # Convertir a float
        num_value = float(value)
        
        # Validaciones por campo
        if field_name == "costos_fijos_mensuales":
            if num_value <= 0:
                return f"❌ Error: Los costos fijos deben ser mayores a 0. Recibido: {num_value}"
        
        elif field_name == "costo_variable_unitario":
            if num_value < 0:
                return f"❌ Error: El costo variable no puede ser negativo. Recibido: {num_value}"
        
        elif field_name == "precio_venta_unitario":
            if num_value <= 0:
                return f"❌ Error: El precio de venta debe ser mayor a 0. Recibido: {num_value}"
            # Validar que precio > costo variable si se proporciona
            if costo_variable_unitario is not None and num_value <= costo_variable_unitario:
                return f"❌ Error: El precio de venta ({num_value}) debe ser mayor que el costo variable ({costo_variable_unitario})"
        
        elif field_name == "volumen_ventas_estimado":
            if num_value <= 0 or num_value != int(num_value):
                return f"❌ Error: El volumen de ventas debe ser un número entero mayor a 0. Recibido: {num_value}"
        
        elif field_name == "inversion_inicial":
            if num_value < 0:
                return f"❌ Error: La inversión inicial no puede ser negativa. Recibido: {num_value}"
        
        logger.info(f"Dato validado: {field_name} = {num_value}")
        return f"✅ Dato válido: {field_name} = {num_value}"
        
    except ValueError:
        return f"❌ Error: El valor '{value}' no es un número válido para {field_name}"
