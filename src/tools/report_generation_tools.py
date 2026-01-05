"""Report Generation Agent tools - Complete implementations."""
import logging
from typing import Annotated
from datetime import datetime
from src.models.financial_data import BusinessInputData
from src.models.reports import Alert

logger = logging.getLogger(__name__)


def generate_charts(data: dict
) -> str:
    """
    Genera descripciones de gráficos financieros.
    
    Nota: Esta implementación genera descripciones de gráficos.
    Para generar gráficos reales con matplotlib, se requiere implementación adicional.
    """
    try:
        # Leer datos
        input_data_file = state.get("files", {}).get("/business_data/input_data.json")
        if not input_data_file:
            return "❌ Error: No se encontraron datos de entrada."
        
        data = BusinessInputData(**input_data_file["data"])
        
        # Calcular métricas para gráficos
        ventas_totales = data.precio_venta_unitario * data.volumen_ventas_estimado
        costos_totales = data.costos_fijos_mensuales + (data.costo_variable_unitario * data.volumen_ventas_estimado)
        pe_unidades = data.costos_fijos_mensuales / (data.precio_venta_unitario - data.costo_variable_unitario)
        
        # Definir gráficos a generar
        charts = {
            "grafico_punto_equilibrio": {
                "tipo": "Líneas",
                "descripcion": "Muestra costos totales, ingresos totales y punto de equilibrio",
                "eje_x": "Unidades vendidas",
                "eje_y": "Dinero ($)",
                "lineas": [
                    {"nombre": "Ingresos", "formula": f"y = {data.precio_venta_unitario} * x"},
                    {"nombre": "Costos Totales", "formula": f"y = {data.costos_fijos_mensuales} + {data.costo_variable_unitario} * x"},
                    {"nombre": "Punto de Equilibrio", "valor": f"{pe_unidades:.0f} unidades, ${pe_unidades * data.precio_venta_unitario:,.2f}"}
                ]
            },
            "grafico_composicion_costos": {
                "tipo": "Pastel",
                "descripcion": "Desglose de costos fijos vs variables",
                "datos": [
                    {"categoria": "Costos Fijos", "valor": data.costos_fijos_mensuales, "porcentaje": f"{data.costos_fijos_mensuales/costos_totales*100:.1f}%"},
                    {"categoria": "Costos Variables", "valor": data.costo_variable_unitario * data.volumen_ventas_estimado, "porcentaje": f"{(data.costo_variable_unitario * data.volumen_ventas_estimado)/costos_totales*100:.1f}%"}
                ]
            },
            "grafico_utilidad": {
                "tipo": "Barras",
                "descripcion": "Comparación de ventas, costos y utilidad",
                "datos": [
                    {"categoria": "Ventas", "valor": ventas_totales},
                    {"categoria": "Costos", "valor": costos_totales},
                    {"categoria": "Utilidad", "valor": ventas_totales - costos_totales}
                ]
            }
        }
        
        # Guardar descripciones de gráficos
        if "files" not in state:
            state["files"] = {}
        
        state["files"]["/reports/charts/chart_descriptions.json"] = {
            "data": charts,
            "content": json.dumps(charts, indent=2, ensure_ascii=False)
        }
        
        message = f"""✅ Descripciones de gráficos generadas:

1. 📊 Gráfico de Punto de Equilibrio
   - Muestra intersección de ingresos y costos
   - Punto de equilibrio: {pe_unidades:.0f} unidades

2. 🥧 Gráfico de Composición de Costos
   - Costos fijos: ${data.costos_fijos_mensuales:,.2f} ({data.costos_fijos_mensuales/costos_totales*100:.1f}%)
   - Costos variables: ${data.costo_variable_unitario * data.volumen_ventas_estimado:,.2f} ({(data.costo_variable_unitario * data.volumen_ventas_estimado)/costos_totales*100:.1f}%)

3. 📈 Gráfico de Utilidad
   - Comparación visual de ventas, costos y utilidad

Guardado en: /reports/charts/chart_descriptions.json

Nota: Para generar gráficos visuales, implementa matplotlib en esta herramienta."""
        
        logger.info("Descripciones de gráficos generadas")
        
        return message
        
    except Exception as e:
        logger.error(f"Error generando gráficos: {str(e)}")
        return f"❌ Error al generar gráficos: {str(e)}"



def create_pdf_report(data: dict
) -> str:
    """
    Crea estructura de reporte PDF.
    
    Nota: Esta implementación genera la estructura del reporte.
    Para generar PDF real con reportlab, se requiere implementación adicional.
    """
    try:
        # Leer todos los datos necesarios
        input_data_file = state.get("files", {}).get("/business_data/input_data.json")
        if not input_data_file:
            return "❌ Error: No se encontraron datos de entrada."
        
        data = BusinessInputData(**input_data_file["data"])
        
        # Calcular métricas
        ventas_totales = data.precio_venta_unitario * data.volumen_ventas_estimado
        costos_totales = data.costos_fijos_mensuales + (data.costo_variable_unitario * data.volumen_ventas_estimado)
        utilidad_neta = ventas_totales - costos_totales
        ros = (utilidad_neta / ventas_totales * 100) if ventas_totales > 0 else 0
        pe_unidades = data.costos_fijos_mensuales / (data.precio_venta_unitario - data.costo_variable_unitario)
        
        # Crear estructura del reporte
        report_structure = {
            "metadata": {
                "titulo": f"Análisis Financiero - {data.nombre_negocio}",
                "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "tipo_negocio": data.tipo_negocio
            },
            "secciones": [
                {
                    "numero": 1,
                    "titulo": "Resumen Ejecutivo",
                    "contenido": {
                        "utilidad_neta_mensual": f"${utilidad_neta:,.2f}",
                        "rentabilidad": f"{ros:.2f}%",
                        "punto_equilibrio": f"{pe_unidades:.0f} unidades",
                        "viabilidad": "Viable" if utilidad_neta > 0 else "No viable con parámetros actuales"
                    }
                },
                {
                    "numero": 2,
                    "titulo": "Datos de Entrada",
                    "contenido": {
                        "costos_fijos": f"${data.costos_fijos_mensuales:,.2f}/mes",
                        "costo_variable_unitario": f"${data.costo_variable_unitario:,.2f}",
                        "precio_venta": f"${data.precio_venta_unitario:,.2f}",
                        "volumen_estimado": f"{data.volumen_ventas_estimado} unidades/mes"
                    }
                },
                {
                    "numero": 3,
                    "titulo": "Métricas Financieras",
                    "contenido": {
                        "ventas_totales": f"${ventas_totales:,.2f}",
                        "costos_totales": f"${costos_totales:,.2f}",
                        "utilidad_neta": f"${utilidad_neta:,.2f}",
                        "ros": f"{ros:.2f}%",
                        "punto_equilibrio_unidades": f"{pe_unidades:.0f}",
                        "punto_equilibrio_dinero": f"${pe_unidades * data.precio_venta_unitario:,.2f}"
                    }
                },
                {
                    "numero": 4,
                    "titulo": "Gráficos",
                    "contenido": "Referencias a gráficos generados"
                },
                {
                    "numero": 5,
                    "titulo": "Conclusiones y Recomendaciones",
                    "contenido": _generate_recommendations(utilidad_neta, ros, pe_unidades, data.volumen_ventas_estimado)
                }
            ]
        }
        
        # Guardar estructura
        if "files" not in state:
            state["files"] = {}
        
        state["files"]["/reports/final_report_structure.json"] = {
            "data": report_structure,
            "content": json.dumps(report_structure, indent=2, ensure_ascii=False)
        }
        
        message = f"""✅ Estructura de reporte PDF generada:

📄 Reporte: {data.nombre_negocio}
📅 Fecha: {datetime.now().strftime("%Y-%m-%d")}

Secciones incluidas:
1. ✅ Resumen Ejecutivo
2. ✅ Datos de Entrada
3. ✅ Métricas Financieras
4. ✅ Gráficos
5. ✅ Conclusiones y Recomendaciones

Guardado en: /reports/final_report_structure.json

Nota: Para generar PDF real, implementa reportlab en esta herramienta."""
        
        logger.info(f"Estructura de reporte PDF generada para {data.nombre_negocio}")
        
        return message
        
    except Exception as e:
        logger.error(f"Error creando reporte PDF: {str(e)}")
        return f"❌ Error al crear reporte PDF: {str(e)}"


def _generate_recommendations(utilidad_neta, ros, pe_unidades, volumen_estimado):
    """Genera recomendaciones basadas en métricas."""
    recommendations = []
    
    if utilidad_neta < 0:
        recommendations.append("⚠️ CRÍTICO: El negocio genera pérdidas. Considere reducir costos o aumentar precios.")
    elif utilidad_neta < 1000:
        recommendations.append("⚠️ Utilidad baja. Busque oportunidades para mejorar márgenes.")
    else:
        recommendations.append("✅ El negocio es rentable.")
    
    if ros < 10:
        recommendations.append("⚠️ Rentabilidad sobre ventas baja (<10%). Optimice estructura de costos.")
    elif ros < 20:
        recommendations.append("✓ Rentabilidad aceptable. Hay espacio para mejora.")
    else:
        recommendations.append("✅ Excelente rentabilidad sobre ventas.")
    
    if pe_unidades > volumen_estimado:
        recommendations.append("⚠️ CRÍTICO: Punto de equilibrio mayor que ventas estimadas. Revise modelo de negocio.")
    elif pe_unidades > volumen_estimado * 0.8:
        recommendations.append("⚠️ Punto de equilibrio muy cercano a ventas estimadas. Poco margen de seguridad.")
    else:
        recommendations.append("✅ Margen de seguridad adecuado sobre punto de equilibrio.")
    
    return recommendations



def create_excel_report(data: dict
) -> str:
    """
    Crea estructura de reporte Excel.
    
    Nota: Esta implementación genera la estructura del Excel.
    Para generar archivo Excel real con openpyxl, se requiere implementación adicional.
    """
    try:
        # Leer datos
        input_data_file = state.get("files", {}).get("/business_data/input_data.json")
        if not input_data_file:
            return "❌ Error: No se encontraron datos de entrada."
        
        data = BusinessInputData(**input_data_file["data"])
        
        # Crear estructura de hojas
        excel_structure = {
            "archivo": f"{data.nombre_negocio}_analisis_financiero.xlsx",
            "hojas": [
                {
                    "nombre": "Datos de Entrada",
                    "columnas": ["Campo", "Valor"],
                    "datos": [
                        ["Nombre del Negocio", data.nombre_negocio],
                        ["Tipo de Negocio", data.tipo_negocio],
                        ["Costos Fijos Mensuales", f"${data.costos_fijos_mensuales:,.2f}"],
                        ["Costo Variable Unitario", f"${data.costo_variable_unitario:,.2f}"],
                        ["Precio de Venta Unitario", f"${data.precio_venta_unitario:,.2f}"],
                        ["Volumen Ventas Estimado", data.volumen_ventas_estimado],
                        ["Inversión Inicial", f"${data.inversion_inicial:,.2f}" if data.inversion_inicial else "N/A"]
                    ]
                },
                {
                    "nombre": "Métricas Básicas",
                    "columnas": ["Métrica", "Valor"],
                    "datos": "Calculadas desde /calculations/basic_metrics.json"
                },
                {
                    "nombre": "Flujo de Efectivo",
                    "columnas": ["Mes", "Entradas", "Salidas", "Flujo Neto", "Saldo Acumulado"],
                    "datos": "Desde /analysis/cashflow_projection.json si existe"
                },
                {
                    "nombre": "Escenarios",
                    "columnas": ["Escenario", "Ventas", "Costos", "Utilidad", "ROS"],
                    "datos": "Desde /scenarios/ si existen"
                },
                {
                    "nombre": "Fórmulas",
                    "columnas": ["Fórmula", "Descripción"],
                    "datos": [
                        ["Costos Totales", "Costos Fijos + (Costo Variable × Volumen)"],
                        ["Punto Equilibrio (und)", "Costos Fijos / (Precio - Costo Variable)"],
                        ["Utilidad Bruta", "Ventas - Costos Variables"],
                        ["Utilidad Neta", "Ventas - Costos Totales"],
                        ["ROS", "(Utilidad Neta / Ventas) × 100"],
                        ["ROI", "(Utilidad Neta Anual / Inversión) × 100"]
                    ]
                }
            ]
        }
        
        # Guardar estructura
        if "files" not in state:
            state["files"] = {}
        
        state["files"]["/reports/excel_structure.json"] = {
            "data": excel_structure,
            "content": json.dumps(excel_structure, indent=2, ensure_ascii=False)
        }
        
        message = f"""✅ Estructura de reporte Excel generada:

📊 Archivo: {excel_structure['archivo']}

Hojas incluidas:
1. ✅ Datos de Entrada
2. ✅ Métricas Básicas
3. ✅ Flujo de Efectivo
4. ✅ Escenarios
5. ✅ Fórmulas

Guardado en: /reports/excel_structure.json

Nota: Para generar archivo Excel real, implementa openpyxl en esta herramienta."""
        
        logger.info("Estructura de Excel generada")
        
        return message
        
    except Exception as e:
        logger.error(f"Error creando Excel: {str(e)}")
        return f"❌ Error al crear Excel: {str(e)}"



def generate_alerts(data: dict
) -> str:
    """
    Genera alertas basadas en análisis financiero.
    """
    try:
        # Leer datos
        input_data_file = state.get("files", {}).get("/business_data/input_data.json")
        if not input_data_file:
            return "❌ Error: No se encontraron datos de entrada."
        
        data = BusinessInputData(**input_data_file["data"])
        
        # Calcular métricas
        ventas_totales = data.precio_venta_unitario * data.volumen_ventas_estimado
        costos_totales = data.costos_fijos_mensuales + (data.costo_variable_unitario * data.volumen_ventas_estimado)
        utilidad_neta = ventas_totales - costos_totales
        ros = (utilidad_neta / ventas_totales * 100) if ventas_totales > 0 else 0
        pe_unidades = data.costos_fijos_mensuales / (data.precio_venta_unitario - data.costo_variable_unitario)
        
        # Generar alertas
        alerts = []
        
        # Alertas críticas
        if pe_unidades > data.volumen_ventas_estimado:
            alerts.append(Alert(
                tipo="critica",
                mensaje=f"Punto de equilibrio ({pe_unidades:.0f} und) MAYOR que ventas proyectadas ({data.volumen_ventas_estimado} und). Negocio NO viable."
            ))
        
        if utilidad_neta < 0:
            alerts.append(Alert(
                tipo="critica",
                mensaje=f"Utilidad neta NEGATIVA (${utilidad_neta:,.2f}). El negocio genera pérdidas."
            ))
        
        # Alertas de advertencia
        if ros < 10 and utilidad_neta > 0:
            alerts.append(Alert(
                tipo="advertencia",
                mensaje=f"Rentabilidad baja (ROS: {ros:.2f}%). Considere optimizar costos o aumentar precios."
            ))
        
        if pe_unidades > data.volumen_ventas_estimado * 0.8:
            alerts.append(Alert(
                tipo="advertencia",
                mensaje=f"Punto de equilibrio muy cercano a ventas estimadas. Poco margen de seguridad."
            ))
        
        if data.inversion_inicial and data.inversion_inicial > 0:
            roi_anual = ((utilidad_neta * 12) / data.inversion_inicial * 100)
            if roi_anual < 15:
                alerts.append(Alert(
                    tipo="advertencia",
                    mensaje=f"ROI anual bajo ({roi_anual:.2f}%). La inversión podría no ser atractiva."
                ))
        
        # Alertas informativas
        if utilidad_neta > 0 and ros >= 20:
            alerts.append(Alert(
                tipo="informacion",
                mensaje=f"Excelente rentabilidad (ROS: {ros:.2f}%). El negocio es muy rentable."
            ))
        
        if pe_unidades < data.volumen_ventas_estimado * 0.5:
            alerts.append(Alert(
                tipo="informacion",
                mensaje=f"Buen margen de seguridad. Punto de equilibrio al {(pe_unidades/data.volumen_ventas_estimado*100):.1f}% de ventas estimadas."
            ))
        
        # Si no hay alertas, agregar mensaje positivo
        if not alerts:
            alerts.append(Alert(
                tipo="informacion",
                mensaje="No se detectaron situaciones críticas. El negocio presenta métricas saludables."
            ))
        
        # Guardar alertas
        alerts_data = {
            "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_alertas": len(alerts),
            "alertas_por_tipo": {
                "criticas": len([a for a in alerts if a.tipo == "critica"]),
                "advertencias": len([a for a in alerts if a.tipo == "advertencia"]),
                "informativas": len([a for a in alerts if a.tipo == "informacion"])
            },
            "alertas": [a.model_dump() for a in alerts]
        }
        
        if "files" not in state:
            state["files"] = {}
        
        state["files"]["/reports/alerts.json"] = {
            "data": alerts_data,
            "content": json.dumps(alerts_data, indent=2, ensure_ascii=False)
        }
        
        # Generar mensaje
        criticas = [a for a in alerts if a.tipo == "critica"]
        advertencias = [a for a in alerts if a.tipo == "advertencia"]
        informativas = [a for a in alerts if a.tipo == "informacion"]
        
        message = f"""✅ Alertas generadas ({len(alerts)} total):

🔴 CRÍTICAS ({len(criticas)}):
{chr(10).join(['- ' + a.mensaje for a in criticas]) if criticas else '- Ninguna'}

⚠️ ADVERTENCIAS ({len(advertencias)}):
{chr(10).join(['- ' + a.mensaje for a in advertencias]) if advertencias else '- Ninguna'}

ℹ️ INFORMATIVAS ({len(informativas)}):
{chr(10).join(['- ' + a.mensaje for a in informativas]) if informativas else '- Ninguna'}

Guardado en: /reports/alerts.json"""
        
        logger.info(f"Alertas generadas: {len(criticas)} críticas, {len(advertencias)} advertencias, {len(informativas)} informativas")
        
        return message
        
    except Exception as e:
        logger.error(f"Error generando alertas: {str(e)}")
        return f"❌ Error al generar alertas: {str(e)}"

