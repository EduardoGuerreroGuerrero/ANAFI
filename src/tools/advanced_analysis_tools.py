"""Advanced Analysis Agent tools - Complete implementations."""
import logging
from src.models.financial_data import BusinessInputData, MonthlyFlow, CashflowProjection

logger = logging.getLogger(__name__)


def project_cashflow(
    data: dict,
    months: int = 12,
) -> str:
    """
    Proyecta flujo de efectivo mensual.
    
    Asume que las ventas y costos se mantienen constantes mes a mes.
    """
    try:
        # Validar parámetros
        if months < 1 or months > 24:
            return "❌ Error: El número de meses debe estar entre 1 y 24."
        
        # Validar datos de entrada
        business_data = BusinessInputData(**data)
        
        # Calcular flujos mensuales
        ventas_mensuales = business_data.precio_venta_unitario * business_data.volumen_ventas_estimado
        costos_variables_mensuales = business_data.costo_variable_unitario * business_data.volumen_ventas_estimado
        costos_totales_mensuales = business_data.costos_fijos_mensuales + costos_variables_mensuales
        flujo_neto_mensual = ventas_mensuales - costos_totales_mensuales
        
        # Proyectar flujos
        flujos_mensuales = []
        saldo_acumulado = 0
        meses_negativos_consecutivos = 0
        
        for mes in range(1, months + 1):
            saldo_acumulado += flujo_neto_mensual
            
            flujo = MonthlyFlow(
                mes=mes,
                entradas=ventas_mensuales,
                salidas=costos_totales_mensuales,
                flujo_neto=flujo_neto_mensual,
                saldo_acumulado=saldo_acumulado
            )
            flujos_mensuales.append(flujo)
            
            # Contar meses negativos consecutivos
            if flujo_neto_mensual < 0:
                meses_negativos_consecutivos += 1
            else:
                meses_negativos_consecutivos = 0
        
        # Generar alertas
        alertas = []
        if flujo_neto_mensual < 0:
            alertas.append("⚠️ ALERTA CRÍTICA: El flujo neto mensual es NEGATIVO. El negocio pierde dinero cada mes.")
        
        if meses_negativos_consecutivos > 3:
            alertas.append(f"⚠️ ALERTA DE LIQUIDEZ: Flujo negativo durante {meses_negativos_consecutivos} meses consecutivos.")
        
        if saldo_acumulado < 0:
            alertas.append(f"⚠️ ALERTA DE INSOLVENCIA: El saldo acumulado es negativo (${saldo_acumulado:,.2f}).")
        
        # Crear proyección
        projection = CashflowProjection(
            proyeccion_meses=months,
            flujos_mensuales=flujos_mensuales,
            alertas=alertas
        )
        
        # Generar mensaje
        alertas_msg = "\n".join(alertas) if alertas else ""
        
        message = f"""✅ Proyección de flujo de efectivo generada ({months} meses):

Flujo mensual:
- Entradas: ${ventas_mensuales:,.2f}
- Salidas: ${costos_totales_mensuales:,.2f}
- Flujo neto: ${flujo_neto_mensual:,.2f}

Saldo acumulado al mes {months}: ${saldo_acumulado:,.2f}

{alertas_msg}"""
        
        logger.info(f"Proyección de flujo de efectivo: {months} meses, saldo final: ${saldo_acumulado:,.2f}")
        
        return message
        
    except Exception as e:
        logger.error(f"Error proyectando flujo de efectivo: {str(e)}")
        return f"❌ Error al proyectar flujo de efectivo: {str(e)}"


def generate_income_statement(data: dict) -> str:
    """
    Genera un estado de resultados simplificado.
    
    Estructura:
    Ventas Totales
    (-) Costos Variables
    = Utilidad Bruta
    (-) Costos Fijos
    = Utilidad Neta
    """
    try:
        # Validar datos de entrada
        business_data = BusinessInputData(**data)
        
        # Calcular componentes del estado de resultados
        ventas_totales = business_data.precio_venta_unitario * business_data.volumen_ventas_estimado
        costos_variables_totales = business_data.costo_variable_unitario * business_data.volumen_ventas_estimado
        utilidad_bruta = ventas_totales - costos_variables_totales
        costos_fijos = business_data.costos_fijos_mensuales
        utilidad_neta = utilidad_bruta - costos_fijos
        
        # Calcular porcentajes
        margen_bruto_pct = (utilidad_bruta / ventas_totales * 100) if ventas_totales > 0 else 0
        margen_neto_pct = (utilidad_neta / ventas_totales * 100) if ventas_totales > 0 else 0
        
        # Crear estado de resultados
        income_statement = {
            "negocio": business_data.nombre_negocio,
            "periodo": "Mensual",
            "ventas_totales": round(ventas_totales, 2),
            "costos_variables": round(costos_variables_totales, 2),
            "utilidad_bruta": round(utilidad_bruta, 2),
            "margen_bruto_porcentaje": round(margen_bruto_pct, 2),
            "costos_fijos": round(costos_fijos, 2),
            "utilidad_neta": round(utilidad_neta, 2),
            "margen_neto_porcentaje": round(margen_neto_pct, 2)
        }
        
        message = f"""✅ Estado de Resultados generado:

═══════════════════════════════════════
ESTADO DE RESULTADOS - {business_data.nombre_negocio}
Período: Mensual
═══════════════════════════════════════

Ventas Totales                ${ventas_totales:>12,.2f}

(-) Costos Variables          ${costos_variables_totales:>12,.2f}
─────────────────────────────────────────
= Utilidad Bruta              ${utilidad_bruta:>12,.2f}
  Margen Bruto:               {margen_bruto_pct:>12.2f}%

(-) Costos Fijos              ${costos_fijos:>12,.2f}
─────────────────────────────────────────
= Utilidad Neta               ${utilidad_neta:>12,.2f}
  Margen Neto:                {margen_neto_pct:>12.2f}%
═══════════════════════════════════════"""
        
        logger.info(f"Estado de resultados generado: Utilidad neta ${utilidad_neta:,.2f}")
        
        return message
        
    except Exception as e:
        logger.error(f"Error generando estado de resultados: {str(e)}")
        return f"❌ Error al generar estado de resultados: {str(e)}"


def create_business_canvas(data: dict) -> str:
    """
    Crea un Business Model Canvas relacionando bloques con métricas financieras.
    """
    try:
        # Validar datos
        business_data = BusinessInputData(**data)
        
        # Calcular métricas básicas
        ventas_totales = business_data.precio_venta_unitario * business_data.volumen_ventas_estimado
        costos_totales = business_data.costos_fijos_mensuales + (business_data.costo_variable_unitario * business_data.volumen_ventas_estimado)
        utilidad_neta = ventas_totales - costos_totales
        ros = (utilidad_neta / ventas_totales * 100) if ventas_totales > 0 else 0
        
        # Crear Business Model Canvas
        canvas = {
            "negocio": business_data.nombre_negocio,
            "tipo": business_data.tipo_negocio,
            "bloques": {
                "segmentos_clientes": {
                    "descripcion": "Clientes objetivo del negocio",
                    "metricas_relacionadas": {
                        "volumen_ventas_proyectado": business_data.volumen_ventas_estimado,
                        "ventas_totales_mensuales": f"${ventas_totales:,.2f}"
                    }
                },
                "propuesta_valor": {
                    "descripcion": "Valor ofrecido a los clientes",
                    "metricas_relacionadas": {
                        "precio_venta_unitario": f"${business_data.precio_venta_unitario:,.2f}",
                        "margen_contribucion": f"${business_data.precio_venta_unitario - business_data.costo_variable_unitario:,.2f}"
                    }
                },
                "canales": {
                    "descripcion": "Cómo se entrega el valor",
                    "metricas_relacionadas": {
                        "costos_distribucion": "Incluidos en costos variables"
                    }
                },
                "relacion_clientes": {
                    "descripcion": "Tipo de relación con clientes",
                    "metricas_relacionadas": {
                        "costos_marketing": "Incluidos en costos fijos"
                    }
                },
                "fuentes_ingresos": {
                    "descripcion": "Cómo genera ingresos el negocio",
                    "metricas_relacionadas": {
                        "ventas_totales": f"${ventas_totales:,.2f}/mes",
                        "rentabilidad_ventas": f"{ros:.2f}%"
                    }
                },
                "recursos_clave": {
                    "descripcion": "Recursos necesarios para operar",
                    "metricas_relacionadas": {
                        "inversion_inicial": f"${business_data.inversion_inicial:,.2f}" if business_data.inversion_inicial else "No especificada"
                    }
                },
                "actividades_clave": {
                    "descripcion": "Actividades principales del negocio",
                    "metricas_relacionadas": {
                        "costos_variables_totales": f"${business_data.costo_variable_unitario * business_data.volumen_ventas_estimado:,.2f}/mes"
                    }
                },
                "alianzas_clave": {
                    "descripcion": "Socios y proveedores estratégicos",
                    "metricas_relacionadas": {
                        "costos_compartidos": "Parte de costos fijos"
                    }
                },
                "estructura_costos": {
                    "descripcion": "Principales costos del negocio",
                    "metricas_relacionadas": {
                        "costos_fijos": f"${business_data.costos_fijos_mensuales:,.2f}/mes",
                        "costos_variables": f"${business_data.costo_variable_unitario:,.2f}/unidad",
                        "costos_totales": f"${costos_totales:,.2f}/mes",
                        "punto_equilibrio": f"{business_data.costos_fijos_mensuales / (business_data.precio_venta_unitario - business_data.costo_variable_unitario):.0f} unidades"
                    }
                }
            }
        }
        
        message = f"""✅ Business Model Canvas creado para {business_data.nombre_negocio}:

Los 9 bloques del canvas han sido relacionados con tus métricas financieras:

📊 Fuentes de Ingresos: ${ventas_totales:,.2f}/mes (ROS: {ros:.2f}%)
💰 Estructura de Costos: ${costos_totales:,.2f}/mes
👥 Segmentos de Clientes: {business_data.volumen_ventas_estimado} unidades/mes
💎 Propuesta de Valor: ${business_data.precio_venta_unitario:,.2f}/unidad"""
        
        logger.info(f"Business Model Canvas creado para {business_data.nombre_negocio}")
        
        return message
        
    except Exception as e:
        logger.error(f"Error creando Business Canvas: {str(e)}")
        return f"❌ Error al crear Business Canvas: {str(e)}"



