"""Scenario Analysis Agent tools - Complete implementations."""
import logging
from typing import List
from src.models.financial_data import BusinessInputData, BasicMetrics, ScenarioData

logger = logging.getLogger(__name__)


def create_scenario(
    data: dict,
    scenario_type: str,
    parameters: dict = None,
) -> str:
    """
    Crea un escenario financiero modificando parámetros clave.
    
    Tipos predefinidos:
    - pesimista: -20% ventas, +10% costos fijos, +5% costos variables
    - moderado: datos actuales sin cambios
    - optimista: +20% ventas, -5% costos fijos, -5% costos variables
    - personalizado: usa parámetros proporcionados
    """
    try:
        # Validar datos base
        business_data = BusinessInputData(**data)
        
        # Aplicar modificaciones según tipo de escenario
        if scenario_type == "pesimista":
            precio_venta = business_data.precio_venta_unitario
            costo_variable = business_data.costo_variable_unitario * 1.05  # +5%
            volumen_ventas = int(business_data.volumen_ventas_estimado * 0.80)  # -20%
            costos_fijos = business_data.costos_fijos_mensuales * 1.10  # +10%
            nombre = "Escenario Pesimista"
            
        elif scenario_type == "moderado":
            precio_venta = business_data.precio_venta_unitario
            costo_variable = business_data.costo_variable_unitario
            volumen_ventas = business_data.volumen_ventas_estimado
            costos_fijos = business_data.costos_fijos_mensuales
            nombre = "Escenario Moderado (Base)"
            
        elif scenario_type == "optimista":
            precio_venta = business_data.precio_venta_unitario
            costo_variable = business_data.costo_variable_unitario * 0.95  # -5%
            volumen_ventas = int(business_data.volumen_ventas_estimado * 1.20)  # +20%
            costos_fijos = business_data.costos_fijos_mensuales * 0.95  # -5%
            nombre = "Escenario Optimista"
            
        elif scenario_type == "personalizado" and parameters:
            precio_venta = parameters.get("precio_venta", business_data.precio_venta_unitario)
            costo_variable = parameters.get("costo_variable", business_data.costo_variable_unitario)
            volumen_ventas = parameters.get("volumen_ventas", business_data.volumen_ventas_estimado)
            costos_fijos = parameters.get("costos_fijos", business_data.costos_fijos_mensuales)
            nombre = parameters.get("nombre", "Escenario Personalizado")
            
        else:
            return f"❌ Error: Tipo de escenario '{scenario_type}' no válido. Usa: pesimista, moderado, optimista, o personalizado."
        
        # Calcular métricas del escenario
        ventas_totales = precio_venta * volumen_ventas
        costos_variables_totales = costo_variable * volumen_ventas
        costos_totales = costos_fijos + costos_variables_totales
        
        # Punto de equilibrio
        margen_contribucion = precio_venta - costo_variable
        if margen_contribucion > 0:
            pe_unidades = costos_fijos / margen_contribucion
            pe_dinero = pe_unidades * precio_venta
        else:
            pe_unidades = 0
            pe_dinero = 0
        
        # Utilidades
        utilidad_bruta = ventas_totales - costos_variables_totales
        utilidad_neta = ventas_totales - costos_totales
        
        # Rentabilidad
        ros = (utilidad_neta / ventas_totales * 100) if ventas_totales > 0 else 0
        roi_anual = None
        if business_data.inversion_inicial and business_data.inversion_inicial > 0:
            roi_anual = ((utilidad_neta * 12) / business_data.inversion_inicial * 100)
        
        # Crear métricas
        metricas = BasicMetrics(
            costos_totales=round(costos_totales, 2),
            punto_equilibrio_unidades=round(pe_unidades, 2),
            punto_equilibrio_dinero=round(pe_dinero, 2),
            utilidad_bruta=round(utilidad_bruta, 2),
            utilidad_neta=round(utilidad_neta, 2),
            rentabilidad_sobre_ventas=round(ros, 2),
            rentabilidad_sobre_inversion=round(roi_anual, 2) if roi_anual else None
        )
        
        # Crear escenario
        scenario = ScenarioData(
            nombre_escenario=nombre,
            tipo=scenario_type,
            precio_venta=round(precio_venta, 2),
            costo_variable=round(costo_variable, 2),
            volumen_ventas=volumen_ventas,
            costos_fijos=round(costos_fijos, 2),
            metricas_calculadas=metricas
        )
        
        message = f"""✅ {nombre} creado:

Parámetros:
- Precio de venta: ${precio_venta:,.2f}
- Costo variable: ${costo_variable:,.2f}
- Volumen de ventas: {volumen_ventas} unidades
- Costos fijos: ${costos_fijos:,.2f}

Resultados:
- Ventas totales: ${ventas_totales:,.2f}
- Utilidad neta: ${utilidad_neta:,.2f}
- ROS: {ros:.2f}%
- Punto de equilibrio: {pe_unidades:.0f} unidades"""
        
        logger.info(f"Escenario {scenario_type} creado: Utilidad neta ${utilidad_neta:,.2f}")
        
        return message
        
    except Exception as e:
        logger.error(f"Error creando escenario: {str(e)}")
        return f"❌ Error al crear escenario: {str(e)}"



def compare_scenarios(
    data: dict,
    scenario_ids: List[str],
) -> str:
    """
    Compara hasta 3 escenarios y genera tabla comparativa.
    """
    try:
        if len(scenario_ids) > 3:
            return "❌ Error: Máximo 3 escenarios para comparar."
        
        if len(scenario_ids) < 2:
            return "❌ Error: Necesitas al menos 2 escenarios para comparar."
        
        # Leer escenarios
        scenarios = []
        for scenario_id in scenario_ids:
            return f"❌ Error: Escenario '{scenario_id}' no encontrado. Créalo primero."
        
        # Crear comparativa
        comparison = {
            "escenarios_comparados": [s.nombre_escenario for s in scenarios],
            "metricas_comparadas": {}
        }
        
        # Comparar métricas
        for i, scenario in enumerate(scenarios):
            comparison["metricas_comparadas"][scenario.nombre_escenario] = {
                "ventas_totales": scenario.precio_venta * scenario.volumen_ventas,
                "utilidad_neta": scenario.metricas_calculadas.utilidad_neta,
                "ros": scenario.metricas_calculadas.rentabilidad_sobre_ventas,
                "punto_equilibrio_unidades": scenario.metricas_calculadas.punto_equilibrio_unidades,
                "punto_equilibrio_dinero": scenario.metricas_calculadas.punto_equilibrio_dinero
            }
        
        # Generar tabla comparativa
        header = f"{'Métrica':<30} " + " ".join([f"{s.tipo.capitalize():<20}" for s in scenarios])
        separator = "=" * (30 + 20 * len(scenarios))
        
        rows = []
        rows.append(f"{'Ventas Totales':<30} " + " ".join([f"${s.precio_venta * s.volumen_ventas:>18,.2f}" for s in scenarios]))
        rows.append(f"{'Utilidad Neta':<30} " + " ".join([f"${s.metricas_calculadas.utilidad_neta:>18,.2f}" for s in scenarios]))
        rows.append(f"{'ROS (%)':<30} " + " ".join([f"{s.metricas_calculadas.rentabilidad_sobre_ventas:>18.2f}%" for s in scenarios]))
        rows.append(f"{'Punto Equilibrio (und)':<30} " + " ".join([f"{s.metricas_calculadas.punto_equilibrio_unidades:>18.0f}" for s in scenarios]))
        rows.append(f"{'Punto Equilibrio ($)':<30} " + " ".join([f"${s.metricas_calculadas.punto_equilibrio_dinero:>18,.2f}" for s in scenarios]))
        
        message = f"""✅ Comparativa de Escenarios:

{separator}
{header}
{separator}
{chr(10).join(rows)}
{separator}"""
        
        logger.info(f"Comparativa de {len(scenarios)} escenarios generada")
        
        return message
        
    except Exception as e:
        logger.error(f"Error comparando escenarios: {str(e)}")
        return f"❌ Error al comparar escenarios: {str(e)}"



def simulate_parameter_change(
    data: dict,
    parameter: str,
    change_percentage: float,
) -> str:
    """
    Simula el impacto de cambiar una variable específica.
    
    Parámetros válidos: precio_venta, costo_variable, costo_fijo, volumen_ventas
    """
    try:
        # Validar parámetro
        valid_params = ["precio_venta", "costo_variable", "costo_fijo", "volumen_ventas"]
        if parameter not in valid_params:
            return f"❌ Error: Parámetro '{parameter}' no válido. Usa: {', '.join(valid_params)}"
        
        # Validar datos base
        business_data = BusinessInputData(**data)
        
        # Calcular métricas base
        ventas_base = business_data.precio_venta_unitario * business_data.volumen_ventas_estimado
        costos_totales_base = business_data.costos_fijos_mensuales + (business_data.costo_variable_unitario * business_data.volumen_ventas_estimado)
        utilidad_base = ventas_base - costos_totales_base
        
        # Aplicar cambio
        factor = 1 + (change_percentage / 100)
        
        if parameter == "precio_venta":
            nuevo_precio = business_data.precio_venta_unitario * factor
            ventas_nuevo = nuevo_precio * business_data.volumen_ventas_estimado
            costos_totales_nuevo = costos_totales_base
            param_label = "Precio de venta"
            valor_base = f"${business_data.precio_venta_unitario:,.2f}"
            valor_nuevo = f"${nuevo_precio:,.2f}"
            
        elif parameter == "costo_variable":
            nuevo_costo_var = business_data.costo_variable_unitario * factor
            ventas_nuevo = ventas_base
            costos_totales_nuevo = business_data.costos_fijos_mensuales + (nuevo_costo_var * business_data.volumen_ventas_estimado)
            param_label = "Costo variable"
            valor_base = f"${business_data.costo_variable_unitario:,.2f}"
            valor_nuevo = f"${nuevo_costo_var:,.2f}"
            
        elif parameter == "costo_fijo":
            nuevos_costos_fijos = business_data.costos_fijos_mensuales * factor
            ventas_nuevo = ventas_base
            costos_totales_nuevo = nuevos_costos_fijos + (business_data.costo_variable_unitario * business_data.volumen_ventas_estimado)
            param_label = "Costos fijos"
            valor_base = f"${business_data.costos_fijos_mensuales:,.2f}"
            valor_nuevo = f"${nuevos_costos_fijos:,.2f}"
            
        else:  # volumen_ventas
            nuevo_volumen = int(business_data.volumen_ventas_estimado * factor)
            ventas_nuevo = business_data.precio_venta_unitario * nuevo_volumen
            costos_totales_nuevo = business_data.costos_fijos_mensuales + (business_data.costo_variable_unitario * nuevo_volumen)
            param_label = "Volumen de ventas"
            valor_base = f"{business_data.volumen_ventas_estimado} unidades"
            valor_nuevo = f"{nuevo_volumen} unidades"
        
        utilidad_nuevo = ventas_nuevo - costos_totales_nuevo
        cambio_utilidad = utilidad_nuevo - utilidad_base
        cambio_utilidad_pct = (cambio_utilidad / utilidad_base * 100) if utilidad_base != 0 else 0
        
        # Guardar simulación
        simulation = {
            "parametro_modificado": parameter,
            "cambio_porcentaje": change_percentage,
            "valor_base": valor_base,
            "valor_nuevo": valor_nuevo,
            "impacto": {
                "utilidad_base": round(utilidad_base, 2),
                "utilidad_nuevo": round(utilidad_nuevo, 2),
                "cambio_absoluto": round(cambio_utilidad, 2),
                "cambio_porcentual": round(cambio_utilidad_pct, 2)
            }
        }
        
        signo = "+" if change_percentage > 0 else ""
        impacto_signo = "+" if cambio_utilidad > 0 else ""
        
        message = f"""✅ Simulación de cambio en {param_label}:

Cambio aplicado: {signo}{change_percentage}%
- Valor base: {valor_base}
- Valor nuevo: {valor_nuevo}

Impacto en Utilidad Neta:
- Utilidad base: ${utilidad_base:,.2f}
- Utilidad nueva: ${utilidad_nuevo:,.2f}
- Cambio: {impacto_signo}${cambio_utilidad:,.2f} ({impacto_signo}{cambio_utilidad_pct:.2f}%)"""
        
        logger.info(f"Simulación: {parameter} {signo}{change_percentage}% → Impacto: {impacto_signo}${cambio_utilidad:,.2f}")
        
        return message
        
    except Exception as e:
        logger.error(f"Error simulando cambio: {str(e)}")
        return f"❌ Error al simular cambio: {str(e)}"

