# ANAFI Deep Agent - Arquitectura y Diseño Completo

## 1. Visión General

**ANAFI** (Análisis Financiero Inteligente) es un DeepAgent diseñado para ayudar a emprendedores, dueños de PYMES y consultores a realizar análisis financieros completos de sus negocios. El agente calcula métricas clave como punto de equilibrio, rentabilidad, ROI, flujo de efectivo y permite simulación de escenarios predictivos.

### 1.1 Objetivos Principales

- Facilitar análisis financiero sin conocimientos avanzados
- Calcular métricas financieras clave automáticamente
- Permitir proyección de escenarios para toma de decisiones
- Integrar herramientas financieras en una plataforma conversacional

### 1.2 Usuarios Objetivo

- Emprendedores y startups
- Dueños de PYMES
- Consultores empresariales
- Estudiantes de negocios

## 2. Arquitectura del DeepAgent

### 2.1 Estructura Principal

```
ANAFI_AGENT/
├── src/
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── builder.py          # Construcción del deep agent
│   │   └── state.py             # Estado extendido con todos y files
│   ├── agents/
│   │   ├── __init__.py
│   │   └── sub_agents_config.py # Configuración de todos los subagentes
│   ├── prompts/
│   │   ├── __init__.py
│   │   ├── supervisor_prompts.py      # Prompts del supervisor
│   │   ├── sub_agent_prompts.py       # Prompts de subagentes
│   │   ├── tool_description_prompts.py # Descripciones de herramientas
│   │   └── tool_llm_calls_prompts.py  # Prompts internos de herramientas
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── calculate_costs.py
│   │   ├── calculate_breakeven.py
│   │   ├── calculate_profitability.py
│   │   ├── calculate_cashflow.py
│   │   ├── generate_income_statement.py
│   │   ├── create_business_canvas.py
│   │   ├── simulate_scenarios.py
│   │   └── generate_financial_report.py
│   └── models/
│       ├── __init__.py
│       ├── financial_data.py    # Modelos Pydantic para datos financieros
│       └── reports.py           # Modelos para reportes
├── langgraph.json
├── requirements.txt
└── README.md
```

### 2.2 Flujo de Orquestación

El supervisor ANAFI sigue este patrón de delegación:

1. **Recepción de datos** → Delega a `data_input_agent`
2. **Cálculos básicos** → Delega a `basic_calculations_agent`
3. **Análisis avanzado** → Delega a `advanced_analysis_agent`
4. **Análisis predictivo** → Delega a `scenario_analysis_agent`
5. **Generación de reportes** → Delega a `report_generation_agent`

## 3. Sub-Agentes del Sistema

### 3.1 Data Input Agent

**Nombre**: `data_input_agent`

**Descripción**: Responsable de recopilar y validar todos los datos financieros del usuario mediante conversación guiada.

**Herramientas**:
- `validate_financial_data`: Valida que los datos ingresados sean numéricos y estén en rangos lógicos
- `save_business_data`: Guarda los datos del negocio en el estado virtual

**Flujo de trabajo**:
1. Solicita datos básicos (costos fijos, variables, precio de venta, volumen estimado)
2. Valida cada entrada
3. Guarda en `/business_data/input_data.json`

### 3.2 Basic Calculations Agent

**Nombre**: `basic_calculations_agent`

**Descripción**: Ejecuta todos los cálculos financieros fundamentales (costos, punto de equilibrio, utilidad, rentabilidad).

**Herramientas**:
- `calculate_total_costs`: Calcula costos totales (fijos + variables)
- `calculate_breakeven_point`: Calcula punto de equilibrio en unidades y dinero
- `calculate_profit`: Calcula utilidad bruta y neta
- `calculate_profitability_ratios`: Calcula ROS y ROI

**Flujo de trabajo**:
1. Lee `/business_data/input_data.json`
2. Ejecuta cálculos en paralelo
3. Guarda resultados en `/calculations/basic_metrics.json`

### 3.3 Advanced Analysis Agent

**Nombre**: `advanced_analysis_agent`

**Descripción**: Genera análisis financieros avanzados como flujo de efectivo, estado de resultados y Business Model Canvas.

**Herramientas**:
- `project_cashflow`: Proyecta flujo de efectivo mensual
- `generate_income_statement`: Genera estado de resultados simplificado
- `create_business_canvas`: Crea Business Model Canvas interactivo

**Flujo de trabajo**:
1. Lee datos básicos y métricas calculadas
2. Genera proyecciones y análisis
3. Guarda en `/analysis/advanced_metrics.json`

### 3.4 Scenario Analysis Agent

**Nombre**: `scenario_analysis_agent`

**Descripción**: Permite simular diferentes escenarios (pesimista, moderado, optimista) variando parámetros clave.

**Herramientas**:
- `create_scenario`: Crea un escenario con parámetros modificados
- `compare_scenarios`: Compara hasta 3 escenarios
- `simulate_parameter_change`: Simula impacto de cambio en una variable específica

**Flujo de trabajo**:
1. Recibe parámetros de escenarios del usuario
2. Ejecuta simulaciones en paralelo
3. Genera comparativas gráficas
4. Guarda en `/scenarios/scenario_analysis.json`

### 3.5 Report Generation Agent

**Nombre**: `report_generation_agent`

**Descripción**: Consolida todos los análisis y genera reportes finales en PDF/Excel con visualizaciones.

**Herramientas**:
- `generate_charts`: Genera gráficos (punto de equilibrio, flujo de efectivo, comparativa de escenarios)
- `create_pdf_report`: Crea reporte PDF completo
- `create_excel_report`: Exporta datos a Excel
- `generate_alerts`: Genera alertas si hay situaciones críticas

**Flujo de trabajo**:
1. Consolida todos los archivos del estado
2. Genera visualizaciones
3. Crea reportes finales
4. Guarda en `/reports/final_report.pdf` y `/reports/financial_data.xlsx`

## 4. Guardrails y Validaciones

### 4.1 Validaciones de Entrada

- Costos fijos > 0
- Costos variables >= 0
- Precio de venta > costo variable unitario
- Volumen de ventas > 0
- Todos los valores numéricos

### 4.2 Reglas de Negocio

- Si punto de equilibrio > ventas proyectadas → Alerta crítica
- Si flujo de efectivo negativo > 3 meses → Alerta de liquidez
- Si ROI < 0 → Alerta de rentabilidad

### 4.3 Límites de Procesamiento

- Máximo 3 escenarios simultáneos
- Proyección de flujo de efectivo: máximo 24 meses
- Validación de rangos lógicos para todos los inputs

## 5. Middlewares

### 5.1 Logging Middleware

Registra todas las operaciones y cálculos para auditoría en `/logs/anafi_operations.jsonl`

### 5.2 Validation Middleware

Valida datos antes de cada cálculo para evitar errores

### 5.3 State Management Middleware

Gestiona el sistema de archivos virtual y asegura consistencia del estado

## 6. Reglas de Orquestación del Supervisor

### 6.1 Política de Delegación

El supervisor ANAFI **NO ejecuta cálculos directamente**. Su rol es:

1. Gestionar el plan maestro con `write_todos`
2. Delegar trabajo a subagentes con `task`
3. Usar `think_tool` para reflexionar sobre resultados
4. Usar herramientas de inspección (`ls`, `grep`, `read_file`) solo para verificación

### 6.2 Flujo Secuencial Obligatorio

```
FASE 1: Recopilación de Datos
  → data_input_agent

FASE 2: Cálculos Básicos  
  → basic_calculations_agent

FASE 3: Análisis Avanzado (opcional)
  → advanced_analysis_agent

FASE 4: Análisis de Escenarios (opcional)
  → scenario_analysis_agent

FASE 5: Generación de Reportes
  → report_generation_agent
```

### 6.3 Paralelismo

- Los cálculos dentro de cada agente se ejecutan en paralelo cuando son independientes
- Los escenarios se simulan en paralelo
- La generación de gráficos se ejecuta en paralelo

## 7. Sistema de Archivos Virtual

### 7.1 Estructura de Directorios

```
/business_data/
  ├── input_data.json           # Datos ingresados por el usuario
  └── business_info.json        # Información general del negocio

/calculations/
  ├── basic_metrics.json        # Métricas básicas calculadas
  └── cost_breakdown.json       # Desglose detallado de costos

/analysis/
  ├── advanced_metrics.json     # Análisis avanzados
  ├── cashflow_projection.json  # Proyección de flujo de efectivo
  ├── income_statement.json     # Estado de resultados
  └── business_canvas.json      # Business Model Canvas

/scenarios/
  ├── scenario_analysis.json    # Análisis comparativo de escenarios
  ├── scenario_1.json           # Escenario pesimista
  ├── scenario_2.json           # Escenario moderado
  └── scenario_3.json           # Escenario optimista

/reports/
  ├── final_report.pdf          # Reporte PDF completo
  ├── financial_data.xlsx       # Datos exportados a Excel
  └── charts/                   # Gráficos generados
      ├── breakeven_chart.png
      ├── cashflow_chart.png
      └── scenarios_comparison.png

/logs/
  └── anafi_operations.jsonl    # Log de todas las operaciones
```

## 8. Modelos de Datos Pydantic

### 8.1 BusinessInputData

```python
class BusinessInputData(BaseModel):
    nombre_negocio: str
    tipo_negocio: str
    costos_fijos_mensuales: float
    costo_variable_unitario: float
    precio_venta_unitario: float
    volumen_ventas_estimado: int
    inversion_inicial: Optional[float] = None
```

### 8.2 BasicMetrics

```python
class BasicMetrics(BaseModel):
    costos_totales: float
    punto_equilibrio_unidades: float
    punto_equilibrio_dinero: float
    utilidad_bruta: float
    utilidad_neta: float
    rentabilidad_sobre_ventas: float  # ROS
    rentabilidad_sobre_inversion: Optional[float] = None  # ROI
```

### 8.3 CashflowProjection

```python
class MonthlyFlow(BaseModel):
    mes: int
    entradas: float
    salidas: float
    flujo_neto: float
    saldo_acumulado: float

class CashflowProjection(BaseModel):
    proyeccion_meses: int
    flujos_mensuales: List[MonthlyFlow]
    alertas: List[str]
```

### 8.4 ScenarioData

```python
class ScenarioData(BaseModel):
    nombre_escenario: str
    tipo: Literal["pesimista", "moderado", "optimista"]
    precio_venta: float
    costo_variable: float
    volumen_ventas: int
    costos_fijos: float
    metricas_calculadas: BasicMetrics
```

## 9. Próximos Pasos para Implementación

Ver documento `ANAFI_Implementation_Guide.md` para instrucciones detalladas de implementación.
