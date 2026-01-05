# ANAFI Deep Agent - Guía de Implementación Completa

## 1. Introducción

Esta guía te ayudará a construir el agente ANAFI desde cero en la carpeta `ANAFI_AGENT`, siguiendo las abstracciones correctas de LangChain y DeepAgents.

## 2. Prerequisitos

### 2.1 Dependencias Requeridas

Crea `requirements.txt`:

```txt
langchain>=0.1.0
langchain-openai>=0.0.5
langgraph>=0.0.20
deepagents>=0.1.0
pydantic>=2.0.0
python-dotenv>=1.0.0
matplotlib>=3.7.0
pandas>=2.0.0
openpyxl>=3.1.0
reportlab>=4.0.0
```

### 2.2 Variables de Entorno

Crea `.env`:

```env
OPENAI_API_KEY=tu_api_key_aqui
LANGCHAIN_API_KEY=tu_langchain_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=anafi-agent
```

## 3. Estructura de Carpetas

Crea la siguiente estructura:

```
ANAFI_AGENT/
├── .env
├── .gitignore
├── langgraph.json
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── builder.py
│   │   └── state.py
│   ├── agents/
│   │   ├── __init__.py
│   │   └── sub_agents_config.py
│   ├── prompts/
│   │   ├── __init__.py
│   │   ├── supervisor_prompts.py
│   │   ├── sub_agent_prompts.py
│   │   ├── tool_description_prompts.py
│   │   └── tool_llm_calls_prompts.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── validate_financial_data.py
│   │   ├── save_business_data.py
│   │   ├── calculate_costs.py
│   │   ├── calculate_breakeven.py
│   │   ├── calculate_profit.py
│   │   ├── calculate_profitability.py
│   │   ├── project_cashflow.py
│   │   ├── generate_income_statement.py
│   │   ├── create_business_canvas.py
│   │   ├── create_scenario.py
│   │   ├── compare_scenarios.py
│   │   ├── simulate_parameter_change.py
│   │   ├── generate_charts.py
│   │   ├── create_pdf_report.py
│   │   ├── create_excel_report.py
│   │   └── generate_alerts.py
│   └── models/
│       ├── __init__.py
│       ├── financial_data.py
│       └── reports.py
└── tests/
    ├── __init__.py
    └── test_calculations.py
```

## 4. Implementación Paso a Paso

### 4.1 Configuración de LangGraph

**Archivo**: `langgraph.json`

```json
{
    "python_version": "3.11",
    "dependencies": ["."],
    "graphs": {
      "anafi_agent": "./src/graph/builder.py:anafi_financial_agent"
    },
    "env": ".env"
}
```

### 4.2 Estado del Agente

**Archivo**: `src/graph/state.py`

```python
"""State management for ANAFI deep agent with TODO tracking and virtual file systems."""

from typing import Annotated, Literal, Any
from typing_extensions import TypedDict, NotRequired
from langchain.agents import AgentState


class Todo(TypedDict):
    """A structured task item for tracking progress through complex workflows."""
    content: str
    status: Literal["pending", "in_progress", "completed"]


def file_reducer(left, right):
    """Merge two file dictionaries, with right side taking precedence."""
    if left is None:
        return right
    elif right is None:
        return left
    else:
        return {**left, **right}


class DeepAgentState(AgentState):
    """Extended agent state that includes task tracking and virtual file system."""
    todos: NotRequired[list[Todo]]
    files: NotRequired[Annotated[dict[str, Any], file_reducer]]
```

### 4.3 Modelos de Datos

**Archivo**: `src/models/financial_data.py`

```python
from pydantic import BaseModel, Field
from typing import Optional, List, Literal


class BusinessInputData(BaseModel):
    """Datos de entrada del negocio proporcionados por el usuario."""
    nombre_negocio: str = Field(description="Nombre del negocio")
    tipo_negocio: str = Field(description="Tipo de negocio (ej: cafetería, tienda)")
    costos_fijos_mensuales: float = Field(gt=0, description="Costos fijos mensuales")
    costo_variable_unitario: float = Field(ge=0, description="Costo variable por unidad")
    precio_venta_unitario: float = Field(gt=0, description="Precio de venta por unidad")
    volumen_ventas_estimado: int = Field(gt=0, description="Volumen de ventas estimado")
    inversion_inicial: Optional[float] = Field(None, ge=0, description="Inversión inicial (opcional)")


class BasicMetrics(BaseModel):
    """Métricas financieras básicas calculadas."""
    costos_totales: float
    punto_equilibrio_unidades: float
    punto_equilibrio_dinero: float
    utilidad_bruta: float
    utilidad_neta: float
    rentabilidad_sobre_ventas: float  # ROS en porcentaje
    rentabilidad_sobre_inversion: Optional[float] = None  # ROI en porcentaje


class MonthlyFlow(BaseModel):
    """Flujo de efectivo de un mes específico."""
    mes: int
    entradas: float
    salidas: float
    flujo_neto: float
    saldo_acumulado: float


class CashflowProjection(BaseModel):
    """Proyección de flujo de efectivo."""
    proyeccion_meses: int
    flujos_mensuales: List[MonthlyFlow]
    alertas: List[str] = []


class ScenarioData(BaseModel):
    """Datos de un escenario financiero."""
    nombre_escenario: str
    tipo: Literal["pesimista", "moderado", "optimista", "personalizado"]
    precio_venta: float
    costo_variable: float
    volumen_ventas: int
    costos_fijos: float
    metricas_calculadas: BasicMetrics
```

### 4.4 Ejemplo de Herramienta

**Archivo**: `src/tools/calculate_breakeven.py`

```python
import logging
from typing import Annotated
from langchain_core.tools import InjectedState, InjectedToolCallId
from src.graph.state import DeepAgentState
from src.models.financial_data import BusinessInputData

logger = logging.getLogger(__name__)


def calculate_breakeven_point(
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> str:
    """
    Calcula el punto de equilibrio en unidades y en dinero.
    
    Fórmulas:
    - Punto de Equilibrio (unidades) = Costos Fijos / (Precio de Venta - Costo Variable Unitario)
    - Punto de Equilibrio (dinero) = Punto de Equilibrio (unidades) × Precio de Venta
    """
    try:
        # Leer datos de entrada del estado
        input_data_file = state.get("files", {}).get("/business_data/input_data.json")
        if not input_data_file:
            return "Error: No se encontraron datos de entrada. Ejecuta primero data_input_agent."
        
        data = BusinessInputData(**input_data_file["data"])
        
        # Calcular margen de contribución unitario
        margen_contribucion = data.precio_venta_unitario - data.costo_variable_unitario
        
        if margen_contribucion <= 0:
            return "Error: El precio de venta debe ser mayor que el costo variable unitario."
        
        # Calcular punto de equilibrio
        pe_unidades = data.costos_fijos_mensuales / margen_contribucion
        pe_dinero = pe_unidades * data.precio_venta_unitario
        
        # Verificar alerta
        alerta = ""
        if pe_unidades > data.volumen_ventas_estimado:
            alerta = f"⚠️ ALERTA CRÍTICA: El punto de equilibrio ({pe_unidades:.0f} unidades) es mayor que las ventas proyectadas ({data.volumen_ventas_estimado} unidades). El negocio no sería viable con estos parámetros."
        
        # Guardar resultado en el estado (se consolidará después)
        result = {
            "punto_equilibrio_unidades": round(pe_unidades, 2),
            "punto_equilibrio_dinero": round(pe_dinero, 2),
            "alerta": alerta
        }
        
        # Actualizar estado
        if "files" not in state:
            state["files"] = {}
        
        state["files"]["/calculations/breakeven_temp.json"] = {
            "data": result,
            "content": str(result)
        }
        
        message = f"Punto de equilibrio calculado:\\n"
        message += f"- En unidades: {pe_unidades:.2f} unidades\\n"
        message += f"- En dinero: ${pe_dinero:,.2f}\\n"
        if alerta:
            message += f"\\n{alerta}"
        
        logger.info(f"Punto de equilibrio calculado: {pe_unidades:.2f} unidades, ${pe_dinero:,.2f}")
        
        return message
        
    except Exception as e:
        logger.error(f"Error calculando punto de equilibrio: {str(e)}")
        return f"Error al calcular punto de equilibrio: {str(e)}"


# Descripción de la herramienta para el agente
calculate_breakeven_point.description = """
Calcula el punto de equilibrio en unidades y en dinero.

Cuándo usar:
- En paralelo con otros cálculos básicos
- Después de tener los datos de entrada disponibles

Fórmulas:
- Punto de Equilibrio (unidades) = Costos Fijos / (Precio de Venta - Costo Variable Unitario)
- Punto de Equilibrio (dinero) = Punto de Equilibrio (unidades) × Precio de Venta

Alertas generadas:
- Si punto de equilibrio > ventas proyectadas: Alerta crítica de viabilidad
"""
```

### 4.5 Configuración de Sub-Agentes

**Archivo**: `src/agents/sub_agents_config.py`

```python
from src.prompts.sub_agent_prompts import *
from src.tools import *

data_input_agent = {
    "name": "data_input_agent",
    "description": "Delega a este agente para recopilar y validar todos los datos financieros del usuario mediante conversación guiada.",
    "system_prompt": DATA_INPUT_AGENT_INSTRUCTIONS,
    "tools": [
        validate_financial_data,
        save_business_data,
    ],
    "model": "openai:gpt-4o-mini"
}

basic_calculations_agent = {
    "name": "basic_calculations_agent",
    "description": "Delega a este agente para calcular métricas financieras básicas: costos totales, punto de equilibrio, utilidad y rentabilidad.",
    "system_prompt": BASIC_CALCULATIONS_AGENT_INSTRUCTIONS,
    "tools": [
        calculate_total_costs,
        calculate_breakeven_point,
        calculate_profit,
        calculate_profitability_ratios,
    ],
    "model": "openai:gpt-4o-mini"
}

advanced_analysis_agent = {
    "name": "advanced_analysis_agent",
    "description": "Delega a este agente para generar análisis financieros avanzados: flujo de efectivo, estado de resultados y Business Model Canvas.",
    "system_prompt": ADVANCED_ANALYSIS_AGENT_INSTRUCTIONS,
    "tools": [
        project_cashflow,
        generate_income_statement,
        create_business_canvas,
    ],
    "model": "openai:gpt-4o-mini"
}

scenario_analysis_agent = {
    "name": "scenario_analysis_agent",
    "description": "Delega a este agente para simular diferentes escenarios financieros y comparar resultados.",
    "system_prompt": SCENARIO_ANALYSIS_AGENT_INSTRUCTIONS,
    "tools": [
        create_scenario,
        compare_scenarios,
        simulate_parameter_change,
    ],
    "model": "openai:gpt-4o-mini"
}

report_generation_agent = {
    "name": "report_generation_agent",
    "description": "Delega a este agente para consolidar todos los análisis y generar reportes finales en PDF/Excel con visualizaciones.",
    "system_prompt": REPORT_GENERATION_AGENT_INSTRUCTIONS,
    "tools": [
        generate_charts,
        create_pdf_report,
        create_excel_report,
        generate_alerts,
    ],
    "model": "openai:gpt-4o-mini"
}
```

### 4.6 Builder del Deep Agent

**Archivo**: `src/graph/builder.py`

```python
from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model

from src.tools import *
from src.agents.sub_agents_config import *
from src.prompts.supervisor_prompts import *

# Create LLM model
llm_model = init_chat_model(model="openai:gpt-4o-mini")

# Define sub-agents
sub_agents = [
    data_input_agent,
    basic_calculations_agent,
    advanced_analysis_agent,
    scenario_analysis_agent,
    report_generation_agent
]

# Create ANAFI deep agent
anafi_financial_agent = create_deep_agent(
    system_prompt=INSTRUCTIONS_SUPERVISOR,
    subagents=sub_agents,
    model=llm_model
)
```

### 4.7 Exportación de Herramientas

**Archivo**: `src/tools/__init__.py`

```python
from .validate_financial_data import validate_financial_data
from .save_business_data import save_business_data
from .calculate_costs import calculate_total_costs
from .calculate_breakeven import calculate_breakeven_point
from .calculate_profit import calculate_profit
from .calculate_profitability import calculate_profitability_ratios
from .project_cashflow import project_cashflow
from .generate_income_statement import generate_income_statement
from .create_business_canvas import create_business_canvas
from .create_scenario import create_scenario
from .compare_scenarios import compare_scenarios
from .simulate_parameter_change import simulate_parameter_change
from .generate_charts import generate_charts
from .create_pdf_report import create_pdf_report
from .create_excel_report import create_excel_report
from .generate_alerts import generate_alerts

__all__ = [
    "validate_financial_data",
    "save_business_data",
    "calculate_total_costs",
    "calculate_breakeven_point",
    "calculate_profit",
    "calculate_profitability_ratios",
    "project_cashflow",
    "generate_income_statement",
    "create_business_canvas",
    "create_scenario",
    "compare_scenarios",
    "simulate_parameter_change",
    "generate_charts",
    "create_pdf_report",
    "create_excel_report",
    "generate_alerts",
]
```

## 5. Pasos de Implementación

### 5.1 Fase 1: Setup Inicial

1. Crear la estructura de carpetas
2. Instalar dependencias: `pip install -r requirements.txt`
3. Configurar variables de entorno en `.env`
4. Crear archivos `__init__.py` en todas las carpetas

### 5.2 Fase 2: Modelos y Estado

1. Implementar `src/graph/state.py`
2. Implementar `src/models/financial_data.py`
3. Implementar `src/models/reports.py`

### 5.3 Fase 3: Prompts

1. Copiar prompts del documento `ANAFI_System_Prompts.md` a:
   - `src/prompts/supervisor_prompts.py`
   - `src/prompts/sub_agent_prompts.py`
2. Crear descripciones de herramientas en `src/prompts/tool_description_prompts.py`

### 5.4 Fase 4: Herramientas (Implementar en orden)

**Data Input Agent Tools**:
1. `validate_financial_data.py`
2. `save_business_data.py`

**Basic Calculations Agent Tools**:
3. `calculate_costs.py`
4. `calculate_breakeven.py`
5. `calculate_profit.py`
6. `calculate_profitability.py`

**Advanced Analysis Agent Tools**:
7. `project_cashflow.py`
8. `generate_income_statement.py`
9. `create_business_canvas.py`

**Scenario Analysis Agent Tools**:
10. `create_scenario.py`
11. `compare_scenarios.py`
12. `simulate_parameter_change.py`

**Report Generation Agent Tools**:
13. `generate_charts.py`
14. `create_pdf_report.py`
15. `create_excel_report.py`
16. `generate_alerts.py`

### 5.5 Fase 5: Configuración de Agentes

1. Implementar `src/agents/sub_agents_config.py`
2. Implementar `src/graph/builder.py`

### 5.6 Fase 6: Testing

1. Crear tests unitarios en `tests/test_calculations.py`
2. Ejecutar: `pytest tests/`

## 6. Ejecución del Agente

### 6.1 Modo Desarrollo (LangGraph Studio)

```bash
langgraph dev
```

Esto abrirá LangGraph Studio en `http://localhost:8123`

### 6.2 Modo Producción

```python
from src.graph.builder import anafi_financial_agent

# Invocar el agente
result = anafi_financial_agent.invoke({
    "messages": [{"role": "user", "content": "Quiero analizar la viabilidad de mi cafetería"}]
})
```

## 7. Ejemplo de Uso Completo

```python
# Conversación de ejemplo
messages = [
    {"role": "user", "content": "Hola, quiero analizar la viabilidad de mi cafetería"},
    # El agente pedirá datos...
    {"role": "user", "content": "Mis costos fijos son $3000 mensuales"},
    {"role": "user", "content": "El costo variable por taza es $1.5"},
    {"role": "user", "content": "Vendo cada taza a $4"},
    {"role": "user", "content": "Estimo vender 1200 tazas al mes"},
    {"role": "user", "content": "Sí, confirmo los datos"},
    # El agente calculará métricas...
    {"role": "user", "content": "Quiero ver escenarios optimista y pesimista"},
    # El agente simulará escenarios...
    {"role": "user", "content": "Genera el reporte final en PDF"},
]

result = anafi_financial_agent.invoke({"messages": messages})
```

## 8. Verificación de la Implementación

### 8.1 Tests Unitarios

Crear `tests/test_calculations.py`:

```python
import pytest
from src.models.financial_data import BusinessInputData
from src.tools.calculate_breakeven import calculate_breakeven_point

def test_breakeven_calculation():
    # Setup
    state = {
        "files": {
            "/business_data/input_data.json": {
                "data": {
                    "nombre_negocio": "Test Café",
                    "tipo_negocio": "cafetería",
                    "costos_fijos_mensuales": 3000,
                    "costo_variable_unitario": 1.5,
                    "precio_venta_unitario": 4.0,
                    "volumen_ventas_estimado": 1200
                }
            }
        }
    }
    
    # Execute
    result = calculate_breakeven_point(state, "test_id")
    
    # Assert
    assert "1200" in result  # Punto de equilibrio en unidades
    assert "4800" in result  # Punto de equilibrio en dinero
```

Ejecutar: `pytest tests/ -v`

### 8.2 Test de Integración

```bash
# Ejecutar el agente con LangGraph Studio
langgraph dev

# Probar conversación completa en la interfaz
```

## 9. Próximos Pasos

1. Implementar todas las herramientas siguiendo el patrón de `calculate_breakeven.py`
2. Agregar logging detallado en cada herramienta
3. Implementar generación de gráficos con matplotlib
4. Implementar generación de PDF con reportlab
5. Implementar exportación a Excel con openpyxl
6. Agregar tests para cada herramienta
7. Documentar casos de uso en README.md

## 10. Recursos Adicionales

- **LangChain Deep Agents**: https://academy.langchain.com/courses/deep-agents-with-langgraph
- **LangGraph Documentation**: https://langchain-ai.github.io/langgraph/
- **Pydantic Documentation**: https://docs.pydantic.dev/
- **Ejemplo de referencia**: Carpeta `ma_change_control_agent`
