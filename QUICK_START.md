# ANAFI Agent - Quick Start Guide

## 📍 Ubicación

El agente ANAFI ha sido creado en:
```
d:\Users\eduguerrero\.gemini\antigravity\playground\eternal-oort\ANAFI_AGENT
```

## 🚀 Pasos para Ejecutar

### 1. Configurar API Keys

Edita el archivo `.env` y agrega tus claves de OpenAI y LangChain:

```env
OPENAI_API_KEY=sk-tu_clave_aqui
LANGCHAIN_API_KEY=tu_langchain_key_aqui
```

### 2. Instalar Dependencias

Abre PowerShell en la carpeta ANAFI_AGENT y ejecuta:

```powershell
cd "d:\Users\eduguerrero\.gemini\antigravity\playground\eternal-oort\ANAFI_AGENT"
pip install -r requirements.txt
```

### 3. Ejecutar el Agente

```powershell
langgraph dev
```

Esto abrirá LangGraph Studio en http://localhost:8123

### 4. Probar el Agente

En LangGraph Studio, escribe:

```
Hola, quiero analizar la viabilidad de mi cafetería
```

El agente te pedirá:
- Costos fijos mensuales
- Costo variable por unidad
- Precio de venta
- Volumen de ventas estimado

Luego calculará automáticamente:
- ✅ Costos totales
- ✅ Punto de equilibrio
- ✅ Utilidad bruta y neta
- ✅ Rentabilidad (ROS y ROI)

## ✅ Funcionalidad Implementada

**Completamente funcional:**
- Recopilación y validación de datos
- Cálculos financieros básicos
- Alertas automáticas

**Pendiente de implementación (stubs):**
- Proyección de flujo de efectivo
- Estado de resultados
- Business Model Canvas
- Simulación de escenarios
- Generación de gráficos
- Reportes PDF/Excel

## 📁 Estructura del Proyecto

```
ANAFI_AGENT/
├── .env                    # Configuración de API keys
├── langgraph.json          # Configuración de LangGraph
├── requirements.txt        # Dependencias
├── README.md              # Documentación básica
├── IMPLEMENTATION_STATUS.md # Estado de implementación
├── src/
│   ├── graph/
│   │   ├── state.py       # Estado del agente
│   │   └── builder.py     # Constructor del deep agent
│   ├── models/
│   │   ├── financial_data.py  # Modelos Pydantic
│   │   └── reports.py         # Modelos de reportes
│   ├── prompts/
│   │   ├── supervisor_prompts.py  # Prompts del supervisor
│   │   └── sub_agent_prompts.py   # Prompts de sub-agentes
│   ├── agents/
│   │   └── sub_agents_config.py   # Configuración de 5 sub-agentes
│   └── tools/
│       ├── validate_financial_data.py  # ✅ Completo
│       ├── save_business_data.py       # ✅ Completo
│       ├── calculate_costs.py          # ✅ Completo
│       ├── calculate_breakeven.py      # ✅ Completo
│       ├── calculate_profit.py         # ✅ Completo
│       ├── calculate_profitability.py  # ✅ Completo
│       ├── advanced_analysis_tools.py  # ⚠️ Stubs
│       ├── scenario_analysis_tools.py  # ⚠️ Stubs
│       └── report_generation_tools.py  # ⚠️ Stubs
└── tests/
    └── __init__.py
```

## 🔧 Próximos Pasos

Para completar la implementación:

1. **Implementar herramientas avanzadas** en:
   - `advanced_analysis_tools.py`
   - `scenario_analysis_tools.py`
   - `report_generation_tools.py`

2. **Agregar tests** en la carpeta `tests/`

3. **Mejorar manejo de errores** en todas las herramientas

## 📚 Documentación Completa

Consulta la carpeta de documentación para:
- Arquitectura detallada
- Descripciones de herramientas
- Guía de implementación paso a paso

## 💡 Ejemplo de Conversación

```
Usuario: Hola, quiero analizar la viabilidad de mi cafetería

ANAFI: ¡Hola! Con gusto te ayudaré a analizar la viabilidad de tu cafetería. 
       Necesito algunos datos financieros. ¿Cuáles son tus costos fijos mensuales?

Usuario: $3000

ANAFI: Perfecto. ¿Cuál es el costo variable por cada taza de café?

Usuario: $1.5

ANAFI: Excelente. ¿A qué precio vendes cada taza?

Usuario: $4

ANAFI: Muy bien. ¿Cuántas tazas estimas vender al mes?

Usuario: 1200

ANAFI: [Ejecuta cálculos...]

       ✅ Análisis completado:
       
       Costos:
       - Costos fijos: $3,000/mes
       - Costos variables: $1,800/mes
       - Costos totales: $4,800/mes
       
       Punto de equilibrio:
       - En unidades: 1,200 tazas/mes
       - En dinero: $4,800/mes
       
       Utilidad:
       - Ventas totales: $4,800/mes
       - Utilidad bruta: $3,000/mes
       - Utilidad neta: $0/mes
       
       ⚠️ ALERTA: Estás exactamente en el punto de equilibrio. 
       No generas ganancias con estos parámetros.
```

## ⚠️ Notas Importantes

1. **API Keys**: Asegúrate de configurar correctamente tus claves en `.env`
2. **Herramientas stub**: Las herramientas marcadas con ⚠️ retornarán mensajes de "en desarrollo"
3. **Funcionalidad básica**: El agente puede realizar análisis financiero básico completo
4. **Copiar carpeta**: Puedes copiar toda la carpeta ANAFI_AGENT a tu ubicación deseada

## 🎯 Para Mover a OneDrive

Si quieres mover el agente a tu ubicación original:

```powershell
# Copiar toda la carpeta
xcopy "d:\Users\eduguerrero\.gemini\antigravity\playground\eternal-oort\ANAFI_AGENT" "D:\Users\eduguerrero\OneDrive - Grupo Procaps\Escritorio\NUEVAS TECNOLOGIAS FARMACEUTICAS\ENTRENAMIENTO\ANTIGRAVITY\PROYECTOS\ANAFI\ANAFI_AGENT" /E /I /H
```

Luego ejecuta `langgraph dev` desde la nueva ubicación.
