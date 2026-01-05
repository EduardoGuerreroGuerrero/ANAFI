# ANAFI Deep Agent - Tool Descriptions

## 1. Data Input Agent Tools

### 1.1 validate_financial_data

**Descripción**: Valida que un campo financiero tenga un valor numérico válido y esté dentro de rangos lógicos.

**Cuándo usar**:
- Inmediatamente después de que el usuario proporcione un dato financiero
- Antes de guardar cualquier dato en el estado

**Parámetros**:
- `field_name (str)`: Nombre del campo a validar (ej: "costos_fijos", "precio_venta")
- `value (Any)`: Valor proporcionado por el usuario

**Salida y efectos en el estado**:
- **ToolMessage**: Confirma si el dato es válido o describe el error específico
- **Estado**: No modifica el estado, solo valida

**Reglas de validación**:
- Costos fijos: > 0
- Costos variables: >= 0
- Precio de venta: > 0 y > costo variable unitario
- Volumen de ventas: > 0 (entero)
- Inversión inicial: >= 0 (opcional)

**Siguiente paso esperado**:
- Si válido: continuar con el siguiente campo o guardar datos
- Si inválido: solicitar el dato nuevamente al usuario

---

### 1.2 save_business_data

**Descripción**: Guarda todos los datos financieros recopilados del usuario en el sistema de archivos virtual.

**Cuándo usar**:
- Después de recopilar y validar TODOS los datos requeridos
- Después de obtener confirmación del usuario

**Parámetros**:
- `data (BusinessInputData)`: Objeto Pydantic con todos los datos del negocio

**Salida y efectos en el estado**:
- **ToolMessage**: Confirma que los datos fueron guardados exitosamente
- **Estado (`state['files']`)**: Crea `/business_data/input_data.json` con los datos validados

**Buenas prácticas**:
- Mostrar un resumen de los datos antes de guardar
- Pedir confirmación explícita del usuario
- Validar todos los campos antes de llamar esta herramienta

**Siguiente paso esperado**:
- Reportar al supervisor que la recopilación de datos está completa

---

## 2. Basic Calculations Agent Tools

### 2.1 calculate_total_costs

**Descripción**: Calcula los costos totales del negocio sumando costos fijos y costos variables totales.

**Cuándo usar**:
- Como primer cálculo del Basic Calculations Agent
- Después de leer `/business_data/input_data.json`

**Parámetros**:
- `state (DeepAgentState)`: Estado inyectado automáticamente
- `tool_call_id (str)`: ID inyectado automáticamente

**Fórmula**:
```
Costos Totales = Costos Fijos + (Costo Variable Unitario × Volumen de Ventas)
```

**Salida y efectos en el estado**:
- **ToolMessage**: Retorna el valor de costos totales calculado
- **Estado**: Almacena el resultado en memoria para consolidación posterior

**Siguiente paso esperado**:
- Ejecutar otros cálculos en paralelo (punto de equilibrio, utilidad, rentabilidad)

---

### 2.2 calculate_breakeven_point

**Descripción**: Calcula el punto de equilibrio en unidades y en dinero.

**Cuándo usar**:
- En paralelo con otros cálculos básicos
- Después de tener los datos de entrada disponibles

**Parámetros**:
- `state (DeepAgentState)`: Estado inyectado automáticamente
- `tool_call_id (str)`: ID inyectado automáticamente

**Fórmulas**:
```
Punto de Equilibrio (unidades) = Costos Fijos / (Precio de Venta - Costo Variable Unitario)
Punto de Equilibrio (dinero) = Punto de Equilibrio (unidades) × Precio de Venta
```

**Salida y efectos en el estado**:
- **ToolMessage**: Retorna punto de equilibrio en unidades y dinero
- **Estado**: Almacena ambos valores para consolidación

**Alertas generadas**:
- Si punto de equilibrio > ventas proyectadas: Alerta crítica de viabilidad

**Siguiente paso esperado**:
- Consolidar con otros cálculos básicos

---

### 2.3 calculate_profit

**Descripción**: Calcula la utilidad bruta y neta del negocio.

**Cuándo usar**:
- En paralelo con otros cálculos básicos
- Requiere datos de entrada y costos totales

**Parámetros**:
- `state (DeepAgentState)`: Estado inyectado automáticamente
- `tool_call_id (str)`: ID inyectado automáticamente

**Fórmulas**:
```
Ventas Totales = Precio de Venta × Volumen de Ventas
Costos Variables Totales = Costo Variable Unitario × Volumen de Ventas
Utilidad Bruta = Ventas Totales - Costos Variables Totales
Utilidad Neta = Ventas Totales - Costos Totales
```

**Salida y efectos en el estado**:
- **ToolMessage**: Retorna utilidad bruta y neta
- **Estado**: Almacena ambos valores

**Alertas generadas**:
- Si utilidad neta < 0: Alerta de pérdidas

**Siguiente paso esperado**:
- Consolidar con otros cálculos básicos

---

### 2.4 calculate_profitability_ratios

**Descripción**: Calcula los ratios de rentabilidad (ROS y ROI).

**Cuándo usar**:
- En paralelo con otros cálculos básicos
- Requiere utilidad neta calculada

**Parámetros**:
- `state (DeepAgentState)`: Estado inyectado automáticamente
- `tool_call_id (str)`: ID inyectado automáticamente

**Fórmulas**:
```
ROS (Rentabilidad sobre Ventas) = (Utilidad Neta / Ventas Totales) × 100
ROI (Rentabilidad sobre Inversión) = (Utilidad Neta / Inversión Inicial) × 100
```

**Salida y efectos en el estado**:
- **ToolMessage**: Retorna ROS y ROI (si aplica)
- **Estado**: Almacena los ratios calculados

**Notas**:
- ROI solo se calcula si el usuario proporcionó inversión inicial
- Los valores se expresan en porcentaje

**Siguiente paso esperado**:
- Consolidar todos los cálculos en `/calculations/basic_metrics.json`

---

## 3. Advanced Analysis Agent Tools

### 3.1 project_cashflow

**Descripción**: Proyecta el flujo de efectivo mensual del negocio para un período determinado.

**Cuándo usar**:
- Cuando el usuario solicita análisis avanzado
- Después de tener métricas básicas calculadas

**Parámetros**:
- `months (int)`: Número de meses a proyectar (default: 12, máximo: 24)
- `state (DeepAgentState)`: Estado inyectado automáticamente
- `tool_call_id (str)`: ID inyectado automáticamente

**Cálculos por mes**:
```
Entradas = Ventas Totales
Salidas = Costos Totales
Flujo Neto = Entradas - Salidas
Saldo Acumulado = Saldo Anterior + Flujo Neto
```

**Salida y efectos en el estado**:
- **ToolMessage**: Resumen de la proyección con alertas si aplica
- **Estado**: Guarda `/analysis/cashflow_projection.json` con proyección completa

**Alertas generadas**:
- Si flujo neto negativo > 3 meses consecutivos: Alerta de liquidez crítica
- Si saldo acumulado < 0 en cualquier mes: Alerta de insolvencia

**Siguiente paso esperado**:
- Ejecutar otros análisis avanzados en paralelo

---

### 3.2 generate_income_statement

**Descripción**: Genera un estado de resultados simplificado del negocio.

**Cuándo usar**:
- En paralelo con otros análisis avanzados
- Requiere métricas básicas calculadas

**Parámetros**:
- `state (DeepAgentState)`: Estado inyectado automáticamente
- `tool_call_id (str)`: ID inyectado automáticamente

**Estructura del estado de resultados**:
```
Ventas Totales
(-) Costos Variables
= Utilidad Bruta
(-) Costos Fijos
= Utilidad Neta
```

**Salida y efectos en el estado**:
- **ToolMessage**: Resumen del estado de resultados
- **Estado**: Guarda `/analysis/income_statement.json`

**Siguiente paso esperado**:
- Consolidar con otros análisis avanzados

---

### 3.3 create_business_canvas

**Descripción**: Genera un Business Model Canvas interactivo relacionando cada bloque con métricas financieras.

**Cuándo usar**:
- Cuando el usuario solicita análisis estratégico
- En paralelo con otros análisis avanzados

**Parámetros**:
- `state (DeepAgentState)`: Estado inyectado automáticamente
- `tool_call_id (str)`: ID inyectado automáticamente

**Bloques del Canvas con métricas relacionadas**:
- **Segmentos de Clientes** → Volumen de ventas proyectado
- **Propuesta de Valor** → Precio de venta unitario
- **Canales** → Costos de distribución (si aplica)
- **Relación con Clientes** → Costos de marketing (si aplica)
- **Fuentes de Ingresos** → Ventas totales, ROS
- **Recursos Clave** → Inversión inicial
- **Actividades Clave** → Costos variables
- **Alianzas Clave** → Costos fijos compartidos (si aplica)
- **Estructura de Costos** → Costos totales, punto de equilibrio

**Salida y efectos en el estado**:
- **ToolMessage**: Confirmación de creación del Canvas
- **Estado**: Guarda `/analysis/business_canvas.json`

**Siguiente paso esperado**:
- Consolidar análisis avanzados

---

## 4. Scenario Analysis Agent Tools

### 4.1 create_scenario

**Descripción**: Crea un escenario financiero modificando parámetros clave del negocio.

**Cuándo usar**:
- Cuando el usuario solicita simulación de escenarios
- Para crear escenarios predefinidos (pesimista, moderado, optimista)

**Parámetros**:
- `scenario_type (Literal["pesimista", "moderado", "optimista", "personalizado"])`: Tipo de escenario
- `parameters (dict)`: Parámetros modificados (opcional para predefinidos)
- `state (DeepAgentState)`: Estado inyectado automáticamente
- `tool_call_id (str)`: ID inyectado automáticamente

**Modificaciones predefinidas**:
- **Pesimista**: -20% ventas, +10% costos fijos, +5% costos variables
- **Moderado**: Sin cambios (datos actuales)
- **Optimista**: +20% ventas, -5% costos fijos, -5% costos variables

**Salida y efectos en el estado**:
- **ToolMessage**: Resumen del escenario creado con métricas calculadas
- **Estado**: Guarda `/scenarios/scenario_{type}.json`

**Siguiente paso esperado**:
- Crear otros escenarios en paralelo
- Ejecutar comparación de escenarios

---

### 4.2 compare_scenarios

**Descripción**: Compara hasta 3 escenarios y genera una tabla y gráfico comparativo.

**Cuándo usar**:
- Después de crear todos los escenarios deseados
- Para ayudar al usuario a tomar decisiones

**Parámetros**:
- `scenario_ids (List[str])`: IDs de los escenarios a comparar (máximo 3)
- `state (DeepAgentState)`: Estado inyectado automáticamente
- `tool_call_id (str)`: ID inyectado automáticamente

**Métricas comparadas**:
- Punto de equilibrio (unidades y dinero)
- Utilidad neta
- Rentabilidad (ROS y ROI)
- Flujo de efectivo proyectado

**Salida y efectos en el estado**:
- **ToolMessage**: Tabla comparativa en texto
- **Estado**: Guarda `/scenarios/scenario_analysis.json` con comparativa completa

**Siguiente paso esperado**:
- Generar reportes finales con la comparativa

---

### 4.3 simulate_parameter_change

**Descripción**: Simula el impacto de cambiar una variable específica en un porcentaje dado.

**Cuándo usar**:
- Cuando el usuario pregunta "¿Qué pasa si...?"
- Para análisis de sensibilidad

**Parámetros**:
- `parameter (Literal["precio_venta", "costo_variable", "costo_fijo", "volumen_ventas"])`: Variable a modificar
- `change_percentage (float)`: Porcentaje de cambio (ej: 10 para +10%, -15 para -15%)
- `state (DeepAgentState)`: Estado inyectado automáticamente
- `tool_call_id (str)`: ID inyectado automáticamente

**Salida y efectos en el estado**:
- **ToolMessage**: Descripción del impacto en métricas clave
- **Estado**: Guarda simulación en `/scenarios/sensitivity_analysis.json`

**Ejemplo de uso**:
```
Usuario: "¿Qué pasa si aumento el precio en un 10%?"
→ simulate_parameter_change(parameter="precio_venta", change_percentage=10)
```

**Siguiente paso esperado**:
- Explicar los resultados al usuario de forma clara

---

## 5. Report Generation Agent Tools

### 5.1 generate_charts

**Descripción**: Genera todos los gráficos necesarios para el reporte financiero.

**Cuándo usar**:
- Como primer paso del Report Generation Agent
- Antes de crear los reportes PDF/Excel

**Parámetros**:
- `state (DeepAgentState)`: Estado inyectado automáticamente
- `tool_call_id (str)`: ID inyectado automáticamente

**Gráficos generados**:
1. **Gráfico de punto de equilibrio**: Muestra costos, ingresos y punto de equilibrio
2. **Gráfico de flujo de efectivo**: Proyección mensual con saldo acumulado
3. **Gráfico comparativo de escenarios**: Comparación de métricas entre escenarios
4. **Gráfico de composición de costos**: Desglose de costos fijos vs variables

**Salida y efectos en el estado**:
- **ToolMessage**: Confirmación de gráficos generados
- **Estado**: Guarda imágenes en `/reports/charts/`

**Siguiente paso esperado**:
- Crear reportes PDF y Excel con los gráficos

---

### 5.2 create_pdf_report

**Descripción**: Crea un reporte PDF completo con todos los análisis, gráficos y recomendaciones.

**Cuándo usar**:
- Después de generar todos los gráficos
- Como penúltimo paso del flujo completo

**Parámetros**:
- `state (DeepAgentState)`: Estado inyectado automáticamente
- `tool_call_id (str)`: ID inyectado automáticamente

**Estructura del reporte PDF**:
1. Portada con nombre del negocio
2. Resumen ejecutivo
3. Datos de entrada
4. Métricas básicas
5. Análisis avanzado (flujo de efectivo, estado de resultados)
6. Análisis de escenarios (si aplica)
7. Gráficos
8. Alertas y recomendaciones
9. Conclusiones

**Salida y efectos en el estado**:
- **ToolMessage**: Confirmación de creación del PDF
- **Estado**: Guarda `/reports/final_report.pdf`

**Siguiente paso esperado**:
- Crear reporte Excel en paralelo

---

### 5.3 create_excel_report

**Descripción**: Exporta todos los datos financieros a un archivo Excel con múltiples hojas.

**Cuándo usar**:
- En paralelo con la creación del PDF
- Para permitir al usuario manipular los datos

**Parámetros**:
- `state (DeepAgentState)`: Estado inyectado automáticamente
- `tool_call_id (str)`: ID inyectado automáticamente

**Hojas del Excel**:
1. **Datos de Entrada**: Todos los datos proporcionados por el usuario
2. **Métricas Básicas**: Costos, punto de equilibrio, utilidad, rentabilidad
3. **Flujo de Efectivo**: Proyección mensual detallada
4. **Escenarios**: Comparativa de escenarios (si aplica)
5. **Fórmulas**: Todas las fórmulas utilizadas para cálculos

**Salida y efectos en el estado**:
- **ToolMessage**: Confirmación de creación del Excel
- **Estado**: Guarda `/reports/financial_data.xlsx`

**Siguiente paso esperado**:
- Generar alertas

---

### 5.4 generate_alerts

**Descripción**: Analiza todos los resultados y genera alertas si hay situaciones críticas o recomendaciones importantes.

**Cuándo usar**:
- Como último paso del Report Generation Agent
- Después de crear todos los reportes

**Parámetros**:
- `state (DeepAgentState)`: Estado inyectado automáticamente
- `tool_call_id (str)`: ID inyectado automáticamente

**Condiciones de alerta**:
- **Crítica**: Punto de equilibrio > ventas proyectadas
- **Crítica**: Flujo de efectivo negativo > 3 meses
- **Advertencia**: Utilidad neta < 10% de ventas
- **Advertencia**: ROI < 15% anual
- **Información**: Recomendaciones de mejora

**Salida y efectos en el estado**:
- **ToolMessage**: Lista de alertas generadas
- **Estado**: Guarda `/reports/alerts.json`

**Siguiente paso esperado**:
- Reportar al supervisor que todos los reportes están listos
