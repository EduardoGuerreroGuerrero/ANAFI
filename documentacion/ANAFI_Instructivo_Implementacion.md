# ANAFI - Instructivo de Implementación Paso a Paso

## ✅ PASO 1: Preparación del Entorno (15 min)

### 1.1 Crear estructura de carpetas

```bash
cd "D:\Users\eduguerrero\OneDrive - Grupo Procaps\Escritorio\NUEVAS TECNOLOGIAS FARMACEUTICAS\ENTRENAMIENTO\ANTIGRAVITY\PROYECTOS\ANAFI"

mkdir ANAFI_AGENT
cd ANAFI_AGENT

# Crear estructura completa
mkdir src
mkdir src\graph
mkdir src\agents
mkdir src\prompts
mkdir src\tools
mkdir src\models
mkdir tests
```

### 1.2 Crear archivos de configuración

**Crear `requirements.txt`:**
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

**Crear `.env`:**
```env
OPENAI_API_KEY=tu_api_key_aqui
LANGCHAIN_API_KEY=tu_langchain_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=anafi-agent
```

**Crear `langgraph.json`:**
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

### 1.3 Instalar dependencias

```bash
pip install -r requirements.txt
```

### 1.4 Crear archivos `__init__.py` vacíos

```bash
# Windows PowerShell
New-Item -ItemType File -Path "src\__init__.py"
New-Item -ItemType File -Path "src\graph\__init__.py"
New-Item -ItemType File -Path "src\agents\__init__.py"
New-Item -ItemType File -Path "src\prompts\__init__.py"
New-Item -ItemType File -Path "src\tools\__init__.py"
New-Item -ItemType File -Path "src\models\__init__.py"
New-Item -ItemType File -Path "tests\__init__.py"
```

---

## ✅ PASO 2: Implementar Estado y Modelos (20 min)

### 2.1 Crear `src/graph/state.py`

Copiar el código del documento **ANAFI_Implementation_Guide.md** sección 4.2.

### 2.2 Crear `src/models/financial_data.py`

Copiar el código del documento **ANAFI_Implementation_Guide.md** sección 4.3.

### 2.3 Crear `src/models/reports.py`

```python
from pydantic import BaseModel
from typing import List

class Alert(BaseModel):
    """Alerta generada por el sistema."""
    tipo: str  # "critica", "advertencia", "informacion"
    mensaje: str
    
class FinancialReport(BaseModel):
    """Reporte financiero completo."""
    nombre_negocio: str
    fecha_generacion: str
    metricas_basicas: dict
    analisis_avanzado: dict
    escenarios: List[dict]
    alertas: List[Alert]
```

---

## ✅ PASO 3: Implementar Prompts (15 min)

### 3.1 Crear `src/prompts/supervisor_prompts.py`

Copiar TODO el contenido del documento **ANAFI_System_Prompts.md** sección 1.

### 3.2 Crear `src/prompts/sub_agent_prompts.py`

Copiar TODO el contenido del documento **ANAFI_System_Prompts.md** sección 2.

### 3.3 Crear `src/prompts/tool_description_prompts.py`

Copiar las descripciones del documento **ANAFI_Tool_Descriptions.md** en formato de constantes Python:

```python
VALIDATE_FINANCIAL_DATA_DESC = """
Valida que un campo financiero tenga un valor numérico válido...
"""

SAVE_BUSINESS_DATA_DESC = """
Guarda todos los datos financieros recopilados...
"""

# ... etc para todas las herramientas
```

---

## ✅ PASO 4: Implementar Herramientas (60-90 min)

### 4.1 Data Input Agent Tools (2 herramientas)

**Crear `src/tools/validate_financial_data.py`:**

```python
from typing import Annotated, Any
from langchain_core.tools import InjectedState, InjectedToolCallId
from src.graph.state import DeepAgentState

def validate_financial_data(
    field_name: str,
    value: Any,
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> str:
    """Valida que un campo financiero sea válido."""
    
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
        
        elif field_name == "volumen_ventas_estimado":
            if num_value <= 0 or num_value != int(num_value):
                return f"❌ Error: El volumen de ventas debe ser un número entero mayor a 0. Recibido: {num_value}"
        
        elif field_name == "inversion_inicial":
            if num_value < 0:
                return f"❌ Error: La inversión inicial no puede ser negativa. Recibido: {num_value}"
        
        return f"✅ Dato válido: {field_name} = {num_value}"
        
    except ValueError:
        return f"❌ Error: El valor '{value}' no es un número válido para {field_name}"

validate_financial_data.description = """Valida campos financieros."""
```

**Crear `src/tools/save_business_data.py`:**

```python
import json
from typing import Annotated
from langchain_core.tools import InjectedState, InjectedToolCallId
from src.graph.state import DeepAgentState
from src.models.financial_data import BusinessInputData

def save_business_data(
    data: dict,
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> str:
    """Guarda los datos del negocio en el estado."""
    
    try:
        # Validar con Pydantic
        business_data = BusinessInputData(**data)
        
        # Guardar en el estado
        if "files" not in state:
            state["files"] = {}
        
        state["files"]["/business_data/input_data.json"] = {
            "data": business_data.model_dump(),
            "content": json.dumps(business_data.model_dump(), indent=2)
        }
        
        return f"✅ Datos guardados exitosamente en /business_data/input_data.json"
        
    except Exception as e:
        return f"❌ Error al guardar datos: {str(e)}"

save_business_data.description = """Guarda datos del negocio."""
```

### 4.2 Basic Calculations Agent Tools (4 herramientas)

**Crear `src/tools/calculate_breakeven.py`:**

Copiar el código completo del documento **ANAFI_Implementation_Guide.md** sección 4.4.

**Crear las otras 3 herramientas siguiendo el mismo patrón:**
- `calculate_costs.py`
- `calculate_profit.py`
- `calculate_profitability.py`

Usa como referencia las fórmulas del documento **ANAFI_Tool_Descriptions.md**.

### 4.3 Advanced Analysis Agent Tools (3 herramientas)

Crear:
- `project_cashflow.py`
- `generate_income_statement.py`
- `create_business_canvas.py`

### 4.4 Scenario Analysis Agent Tools (3 herramientas)

Crear:
- `create_scenario.py`
- `compare_scenarios.py`
- `simulate_parameter_change.py`

### 4.5 Report Generation Agent Tools (4 herramientas)

Crear:
- `generate_charts.py`
- `create_pdf_report.py`
- `create_excel_report.py`
- `generate_alerts.py`

### 4.6 Crear `src/tools/__init__.py`

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

---

## ✅ PASO 5: Configurar Sub-Agentes (10 min)

### 5.1 Crear `src/agents/sub_agents_config.py`

Copiar el código completo del documento **ANAFI_Implementation_Guide.md** sección 4.5.

---

## ✅ PASO 6: Crear Builder del DeepAgent (5 min)

### 6.1 Crear `src/graph/builder.py`

Copiar el código completo del documento **ANAFI_Implementation_Guide.md** sección 4.6.

---

## ✅ PASO 7: Probar el Agente (15 min)

### 7.1 Ejecutar con LangGraph Studio

```bash
langgraph dev
```

Esto abrirá LangGraph Studio en `http://localhost:8123`

### 7.2 Probar conversación de ejemplo

En LangGraph Studio, escribe:

```
Hola, quiero analizar la viabilidad de mi cafetería
```

El agente debería:
1. Saludarte y pedir datos
2. Solicitar costos fijos, variables, precio, volumen
3. Calcular métricas
4. Ofrecer análisis adicionales

---

## 📋 CHECKLIST DE IMPLEMENTACIÓN

### Setup Inicial
- [ ] Estructura de carpetas creada
- [ ] `requirements.txt` creado
- [ ] `.env` configurado con API keys
- [ ] `langgraph.json` creado
- [ ] Dependencias instaladas
- [ ] Archivos `__init__.py` creados

### Estado y Modelos
- [ ] `src/graph/state.py` implementado
- [ ] `src/models/financial_data.py` implementado
- [ ] `src/models/reports.py` implementado

### Prompts
- [ ] `src/prompts/supervisor_prompts.py` implementado
- [ ] `src/prompts/sub_agent_prompts.py` implementado
- [ ] `src/prompts/tool_description_prompts.py` implementado

### Herramientas - Data Input Agent
- [ ] `validate_financial_data.py`
- [ ] `save_business_data.py`

### Herramientas - Basic Calculations Agent
- [ ] `calculate_costs.py`
- [ ] `calculate_breakeven.py`
- [ ] `calculate_profit.py`
- [ ] `calculate_profitability.py`

### Herramientas - Advanced Analysis Agent
- [ ] `project_cashflow.py`
- [ ] `generate_income_statement.py`
- [ ] `create_business_canvas.py`

### Herramientas - Scenario Analysis Agent
- [ ] `create_scenario.py`
- [ ] `compare_scenarios.py`
- [ ] `simulate_parameter_change.py`

### Herramientas - Report Generation Agent
- [ ] `generate_charts.py`
- [ ] `create_pdf_report.py`
- [ ] `create_excel_report.py`
- [ ] `generate_alerts.py`

### Configuración Final
- [ ] `src/tools/__init__.py` con todas las exportaciones
- [ ] `src/agents/sub_agents_config.py` implementado
- [ ] `src/graph/builder.py` implementado

### Testing
- [ ] `langgraph dev` ejecuta sin errores
- [ ] Conversación de prueba funciona
- [ ] Datos se recopilan correctamente
- [ ] Cálculos se ejecutan correctamente

---

## 🚀 ORDEN RECOMENDADO DE IMPLEMENTACIÓN

1. **Día 1 (2-3 horas)**: Setup + Estado + Modelos + Prompts
2. **Día 2 (3-4 horas)**: Data Input Agent + Basic Calculations Agent (6 herramientas)
3. **Día 3 (2-3 horas)**: Advanced Analysis Agent (3 herramientas)
4. **Día 4 (2-3 horas)**: Scenario Analysis Agent (3 herramientas)
5. **Día 5 (3-4 horas)**: Report Generation Agent (4 herramientas)
6. **Día 6 (1-2 horas)**: Configuración final + Testing

**Total estimado: 13-19 horas**

---

## 💡 TIPS IMPORTANTES

### Para implementar herramientas rápido:

1. **Usa el patrón de `calculate_breakeven.py`** como plantilla
2. **Copia la estructura básica**:
   - Imports
   - Función con decoradores `InjectedState` y `InjectedToolCallId`
   - Leer datos del estado
   - Hacer cálculos
   - Guardar resultados en el estado
   - Retornar mensaje descriptivo
   - Agregar `.description`

3. **Las fórmulas están en** `ANAFI_Tool_Descriptions.md`
4. **Los prompts están listos** en `ANAFI_System_Prompts.md`

### Para debugging:

- Usa `logger.info()` en cada herramienta
- Revisa el estado con `ls` en LangGraph Studio
- Prueba cada herramienta individualmente antes de integrar

### Para optimizar:

- Implementa primero las herramientas críticas (Data Input + Basic Calculations)
- Prueba el flujo básico antes de agregar análisis avanzados
- Los reportes PDF/Excel pueden ser simples al inicio

---

## 📞 SOPORTE

Si tienes dudas:
1. Consulta `ANAFI_Tool_Descriptions.md` para fórmulas y lógica
2. Consulta `ANAFI_System_Prompts.md` para comportamiento esperado
3. Consulta `ma_change_control_agent` como referencia de código
4. Revisa LangChain Academy: https://academy.langchain.com/courses/deep-agents-with-langgraph
