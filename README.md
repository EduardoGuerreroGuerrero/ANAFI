# ANAFI - Agente de Análisis Financiero Inteligente

Sistema de análisis financiero conversacional basado en DeepAgents de LangChain.

## 🎯 ¿Qué es ANAFI?

ANAFI es un agente inteligente que ayuda a emprendedores, dueños de PYMES y consultores a realizar análisis financieros completos de sus negocios mediante conversación natural.

### Funcionalidades Principales

✅ **Recopilación de datos** mediante conversación guiada
✅ **Cálculos financieros básicos** (costos, punto de equilibrio, utilidad, rentabilidad)
✅ **Análisis avanzado** (flujo de efectivo, estado de resultados, Business Model Canvas)
✅ **Simulación de escenarios** (pesimista, moderado, optimista, personalizado)
✅ **Generación de reportes** con alertas inteligentes
✅ **Tests completos** para todas las funcionalidades

## 🚀 Quick Start

### 1. Configurar API Keys

Edita el archivo `.env` y agrega tus claves:

```env
OPENAI_API_KEY=sk-tu_clave_aqui
LANGCHAIN_API_KEY=tu_langchain_key_aqui
```

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar Tests

```bash
pytest tests/ -v
```

### 4. Ejecutar el Agente

```bash
langgraph dev
```

Abre http://localhost:8123 y comienza a conversar:

```
Usuario: "Quiero analizar la viabilidad de mi cafetería"
```

## 📚 Documentación Completa

Toda la documentación está en la carpeta **`documentacion/`**:

- 📄 **ANAFI_Executive_Summary.md** - Resumen ejecutivo
- 📄 **ANAFI_Deep_Agent_Architecture.md** - Arquitectura completa
- 📄 **ANAFI_System_Prompts.md** - Prompts del supervisor y sub-agentes
- 📄 **ANAFI_Tool_Descriptions.md** - Descripciones de las 16 herramientas
- 📄 **ANAFI_Implementation_Guide.md** - Guía de implementación
- 📄 **ANAFI_Instructivo_Implementacion.md** - Instructivo paso a paso

👉 **Empieza leyendo**: `documentacion/README.md`

## 🏗️ Estructura del Proyecto

```
ANAFI_AGENT/
├── documentacion/          # Documentación completa
├── src/
│   ├── graph/             # Estado y builder del deep agent
│   ├── models/            # Modelos Pydantic
│   ├── prompts/           # Prompts del sistema
│   ├── agents/            # Configuración de 5 sub-agentes
│   └── tools/             # 16 herramientas implementadas
├── tests/                 # Tests unitarios (50+ casos)
├── requirements.txt       # Dependencias
├── langgraph.json        # Configuración LangGraph
├── .env                  # Variables de entorno
└── IMPLEMENTATION_STATUS.md  # Estado de implementación
```

## 🤖 Arquitectura

ANAFI utiliza 5 sub-agentes especializados:

1. **Data Input Agent** - Recopila y valida datos
2. **Basic Calculations Agent** - Calcula métricas básicas
3. **Advanced Analysis Agent** - Genera análisis avanzados
4. **Scenario Analysis Agent** - Simula escenarios
5. **Report Generation Agent** - Genera reportes y alertas

## 💡 Ejemplo de Uso

```
Usuario: "Hola, quiero analizar mi cafetería"

ANAFI: "¡Perfecto! Necesito algunos datos financieros.
        ¿Cuáles son tus costos fijos mensuales?"

Usuario: "$3000"

ANAFI: "Entendido. ¿Cuál es el costo variable por taza?"

Usuario: "$1.5"

ANAFI: "Perfecto. ¿A qué precio vendes cada taza?"

Usuario: "$4"

ANAFI: "Excelente. ¿Cuántas tazas estimas vender al mes?"

Usuario: "1500"

ANAFI: [Ejecuta cálculos...]

✅ Análisis completado:

Costos:
- Costos totales: $5,250/mes

Punto de equilibrio:
- En unidades: 1,200 tazas/mes
- En dinero: $4,800/mes

Utilidad:
- Ventas totales: $6,000/mes
- Utilidad neta: $750/mes
- ROS: 12.5%

✓ El negocio es viable con estos parámetros.
```

## 🧪 Tests

Ejecutar todos los tests:

```bash
pytest tests/ -v
```

Ejecutar con cobertura:

```bash
pytest tests/ --cov=src --cov-report=html
```

Tests específicos:

```bash
pytest tests/test_calculations.py -v
pytest tests/test_advanced_analysis.py -v
pytest tests/test_scenarios.py -v
```

## 📊 Herramientas Disponibles

### Data Input (2)
- `validate_financial_data` - Valida datos financieros
- `save_business_data` - Guarda datos en el estado

### Basic Calculations (4)
- `calculate_total_costs` - Calcula costos totales
- `calculate_breakeven_point` - Calcula punto de equilibrio
- `calculate_profit` - Calcula utilidad bruta y neta
- `calculate_profitability_ratios` - Calcula ROS y ROI

### Advanced Analysis (3)
- `project_cashflow` - Proyecta flujo de efectivo (hasta 24 meses)
- `generate_income_statement` - Genera estado de resultados
- `create_business_canvas` - Crea Business Model Canvas

### Scenario Analysis (3)
- `create_scenario` - Crea escenarios (pesimista/moderado/optimista)
- `compare_scenarios` - Compara hasta 3 escenarios
- `simulate_parameter_change` - Simula cambios en variables

### Report Generation (4)
- `generate_charts` - Genera descripciones de gráficos
- `create_pdf_report` - Crea estructura de reporte PDF
- `create_excel_report` - Crea estructura de reporte Excel
- `generate_alerts` - Genera alertas inteligentes

## 🔧 Configuración

### Variables de Entorno

Edita `.env`:

```env
OPENAI_API_KEY=tu_clave_openai
LANGCHAIN_API_KEY=tu_clave_langchain
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=anafi-agent
```

### Dependencias

- Python 3.11+
- LangChain >= 0.1.0
- LangGraph >= 0.0.20
- DeepAgents >= 0.1.0
- Pydantic >= 2.0.0
- pytest >= 7.4.0 (para tests)

## 📝 Estado de Implementación

✅ **100% Completo** - Todas las herramientas implementadas y testeadas

Ver `IMPLEMENTATION_STATUS.md` para detalles completos.

## 🎓 Aprendizaje

Este proyecto está basado en:
- [LangChain Academy - Deep Agents](https://academy.langchain.com/courses/deep-agents-with-langgraph)
- Ejemplo de referencia: `ma_change_control_agent`

## 📞 Soporte

Para dudas sobre:
- **Uso del agente**: Consulta `QUICK_START.md`
- **Arquitectura**: Consulta `documentacion/ANAFI_Deep_Agent_Architecture.md`
- **Herramientas**: Consulta `documentacion/ANAFI_Tool_Descriptions.md`
- **Implementación**: Consulta `documentacion/ANAFI_Implementation_Guide.md`

## 📄 Licencia

Este proyecto es un ejemplo educativo basado en LangChain y DeepAgents.

---

**Desarrollado con**: LangChain, LangGraph, DeepAgents, Pydantic
**Versión**: 1.0.0 (Completa)
