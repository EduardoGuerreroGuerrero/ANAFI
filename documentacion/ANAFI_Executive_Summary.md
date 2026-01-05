# ANAFI Deep Agent - Resumen Ejecutivo de la Documentación

## 📋 Descripción General

ANAFI (Análisis Financiero Inteligente) es un DeepAgent diseñado para realizar análisis financieros completos de negocios, calculando métricas clave como punto de equilibrio, rentabilidad, ROI, flujo de efectivo y permitiendo simulación de escenarios predictivos.

## 📚 Documentos Entregados

### 1. ANAFI_Deep_Agent_Architecture.md
**Contenido**:
- Visión general y objetivos del agente
- Estructura completa del proyecto (carpetas y archivos)
- Arquitectura del DeepAgent con 5 sub-agentes
- Flujo de orquestación del supervisor
- Sistema de archivos virtual
- Modelos de datos Pydantic
- Guardrails y validaciones
- Reglas de orquestación

**Secciones clave**:
- 5 Sub-agentes especializados
- Política de delegación del supervisor
- Estructura de directorios virtuales
- Modelos de datos (BusinessInputData, BasicMetrics, CashflowProjection, ScenarioData)

### 2. ANAFI_System_Prompts.md
**Contenido**:
- Prompt completo del supervisor ANAFI
- Prompts de los 5 sub-agentes:
  1. Data Input Agent
  2. Basic Calculations Agent
  3. Advanced Analysis Agent
  4. Scenario Analysis Agent
  5. Report Generation Agent

**Características**:
- Instrucciones detalladas de cada agente
- Flujos de trabajo específicos
- Herramientas asignadas a cada agente
- Límites y restricciones

### 3. ANAFI_Tool_Descriptions.md
**Contenido**:
- Descripciones completas de las 15 herramientas
- Parámetros de entrada y salida
- Fórmulas matemáticas utilizadas
- Cuándo usar cada herramienta
- Efectos en el estado del agente
- Alertas generadas
- Buenas prácticas

**Herramientas documentadas**:
- Data Input: validate_financial_data, save_business_data
- Basic Calculations: calculate_total_costs, calculate_breakeven_point, calculate_profit, calculate_profitability_ratios
- Advanced Analysis: project_cashflow, generate_income_statement, create_business_canvas
- Scenario Analysis: create_scenario, compare_scenarios, simulate_parameter_change
- Report Generation: generate_charts, create_pdf_report, create_excel_report, generate_alerts

### 4. ANAFI_Implementation_Guide.md
**Contenido**:
- Guía paso a paso para implementar el agente desde cero
- Estructura completa de carpetas
- Código de ejemplo para cada componente
- Configuración de LangGraph
- Implementación de modelos Pydantic
- Ejemplo completo de herramienta
- Configuración de sub-agentes
- Builder del DeepAgent
- Tests unitarios
- Instrucciones de ejecución

**Fases de implementación**:
1. Setup inicial (dependencias, .env, estructura)
2. Modelos y estado
3. Prompts
4. Herramientas (16 herramientas en orden)
5. Configuración de agentes
6. Testing

## 🏗️ Arquitectura del Sistema

### Sub-Agentes

1. **Data Input Agent**: Recopila y valida datos financieros del usuario
2. **Basic Calculations Agent**: Calcula métricas básicas (costos, punto de equilibrio, utilidad, rentabilidad)
3. **Advanced Analysis Agent**: Genera flujo de efectivo, estado de resultados y Business Model Canvas
4. **Scenario Analysis Agent**: Simula escenarios (pesimista, moderado, optimista)
5. **Report Generation Agent**: Consolida análisis y genera reportes PDF/Excel

### Flujo de Trabajo

```
Usuario → Supervisor ANAFI
           ↓
    1. Data Input Agent (recopila datos)
           ↓
    2. Basic Calculations Agent (calcula métricas)
           ↓
    3. Advanced Analysis Agent (análisis avanzado - opcional)
           ↓
    4. Scenario Analysis Agent (escenarios - opcional)
           ↓
    5. Report Generation Agent (reportes finales)
           ↓
    Entrega reportes PDF/Excel al usuario
```

### Sistema de Archivos Virtual

```
/business_data/          # Datos de entrada
/calculations/           # Métricas calculadas
/analysis/              # Análisis avanzados
/scenarios/             # Escenarios simulados
/reports/               # Reportes finales
/logs/                  # Logs de operaciones
```

## 🔧 Tecnologías Utilizadas

- **LangChain**: Framework para agentes conversacionales
- **LangGraph**: Orquestación de grafos de agentes
- **DeepAgents**: Abstracción para agentes profundos
- **Pydantic**: Validación de datos
- **Matplotlib**: Generación de gráficos
- **ReportLab**: Generación de PDFs
- **OpenPyXL**: Exportación a Excel

## 📊 Métricas Calculadas

### Básicas
- Costos totales
- Punto de equilibrio (unidades y dinero)
- Utilidad bruta y neta
- Rentabilidad sobre ventas (ROS)
- Rentabilidad sobre inversión (ROI)

### Avanzadas
- Proyección de flujo de efectivo (hasta 24 meses)
- Estado de resultados
- Business Model Canvas

### Escenarios
- Escenario pesimista (-20% ventas, +10% costos)
- Escenario moderado (datos actuales)
- Escenario optimista (+20% ventas, -5% costos)
- Escenarios personalizados

## 🚀 Cómo Usar Esta Documentación

### Para Implementar el Agente

1. **Leer primero**: `ANAFI_Deep_Agent_Architecture.md` para entender la estructura
2. **Revisar prompts**: `ANAFI_System_Prompts.md` para entender el comportamiento
3. **Consultar herramientas**: `ANAFI_Tool_Descriptions.md` para implementar cada tool
4. **Seguir la guía**: `ANAFI_Implementation_Guide.md` paso a paso

### Orden de Implementación Recomendado

1. Setup inicial (carpetas, dependencias, .env)
2. Implementar `state.py` y modelos Pydantic
3. Copiar prompts a archivos correspondientes
4. Implementar herramientas una por una (empezar con Data Input Agent)
5. Configurar sub-agentes en `sub_agents_config.py`
6. Crear builder en `builder.py`
7. Ejecutar con `langgraph dev`
8. Probar conversación completa

## ⚠️ Consideraciones Importantes

### Guardrails
- Validación de todos los inputs numéricos
- Alertas automáticas para situaciones críticas
- Límite de 3 escenarios simultáneos
- Validación de rangos lógicos

### Reglas de Orquestación
- El supervisor NUNCA ejecuta cálculos directamente
- Todos los cálculos se delegan a sub-agentes
- Los sub-agentes ejecutan herramientas en paralelo cuando es posible
- El flujo es secuencial entre fases pero paralelo dentro de cada fase

### Sistema de Archivos Virtual
- Todos los datos se almacenan en el estado del agente
- No hay persistencia real en disco (a menos que se implemente)
- Los archivos se organizan por tipo de análisis
- Los reportes finales sí se generan en disco (PDF/Excel)

## 📖 Ejemplo de Uso

```
Usuario: "Quiero analizar la viabilidad de mi cafetería"
ANAFI: "¡Perfecto! Voy a ayudarte a analizar tu cafetería. Necesito algunos datos..."

Usuario: "Mis costos fijos son $3000 mensuales"
ANAFI: "Entendido. ¿Cuál es el costo variable por cada taza de café?"

Usuario: "El costo variable es $1.5 por taza"
ANAFI: "Perfecto. ¿A qué precio vendes cada taza?"

Usuario: "Vendo cada taza a $4"
ANAFI: "Excelente. ¿Cuántas tazas estimas vender al mes?"

Usuario: "Estimo vender 1200 tazas al mes"
ANAFI: "Confirmado. Déjame calcular las métricas..."

[ANAFI ejecuta cálculos]

ANAFI: "Análisis completado:
- Punto de equilibrio: 1,200 unidades ($4,800)
- Utilidad neta mensual: $1,800
- Rentabilidad sobre ventas: 37.5%

¿Quieres que simule escenarios o genere el reporte final?"
```

## 🎯 Próximos Pasos

1. Implementar todas las herramientas siguiendo `ANAFI_Implementation_Guide.md`
2. Probar cada herramienta individualmente
3. Integrar con LangGraph Studio
4. Realizar pruebas de conversación completa
5. Ajustar prompts según sea necesario
6. Agregar más validaciones y guardrails
7. Mejorar generación de reportes con diseños profesionales

## 📞 Soporte

Para dudas sobre la implementación:
- Consultar LangChain Academy: https://academy.langchain.com/courses/deep-agents-with-langgraph
- Revisar ejemplo de referencia: `ma_change_control_agent`
- Consultar documentación de LangGraph: https://langchain-ai.github.io/langgraph/

---

**Nota**: Esta documentación está diseñada para ser autosuficiente. Contiene toda la información necesaria para implementar el agente ANAFI desde cero, siguiendo las mejores prácticas de LangChain y DeepAgents.
