# ANAFI Agent - Índice de Documentación

Esta carpeta contiene toda la documentación completa del agente ANAFI.

## 📚 Documentos Disponibles

### 1. Resumen Ejecutivo
**Archivo**: `ANAFI_Executive_Summary.md`
- Visión general del proyecto
- Resumen de todos los documentos
- Guía rápida de uso de la documentación
- Estructura del agente
- Ejemplo de conversación

### 2. Arquitectura del Sistema
**Archivo**: `ANAFI_Deep_Agent_Architecture.md`
- Visión general y objetivos
- Estructura completa del proyecto (carpetas y archivos)
- Arquitectura del DeepAgent con 5 sub-agentes
- Flujo de orquestación del supervisor
- Sistema de archivos virtual
- Modelos de datos Pydantic
- Guardrails y validaciones
- Reglas de orquestación

### 3. Prompts del Sistema
**Archivo**: `ANAFI_System_Prompts.md`
- Prompt completo del supervisor ANAFI
- Prompts de los 5 sub-agentes:
  1. Data Input Agent
  2. Basic Calculations Agent
  3. Advanced Analysis Agent
  4. Scenario Analysis Agent
  5. Report Generation Agent
- Instrucciones detalladas de cada agente
- Flujos de trabajo específicos
- Herramientas asignadas a cada agente

### 4. Descripciones de Herramientas
**Archivo**: `ANAFI_Tool_Descriptions.md`
- Descripciones completas de las 16 herramientas
- Parámetros de entrada y salida
- Fórmulas matemáticas utilizadas
- Cuándo usar cada herramienta
- Efectos en el estado del agente
- Alertas generadas
- Buenas prácticas

### 5. Guía de Implementación
**Archivo**: `ANAFI_Implementation_Guide.md`
- Guía paso a paso para implementar el agente desde cero
- Estructura completa de carpetas
- Código de ejemplo para cada componente
- Configuración de LangGraph
- Implementación de modelos Pydantic
- Ejemplo completo de herramienta
- Tests unitarios
- Instrucciones de ejecución

### 6. Instructivo de Implementación
**Archivo**: `ANAFI_Instructivo_Implementacion.md`
- Instructivo paso a paso más conciso
- Comandos específicos de PowerShell
- Checklist completa de implementación
- Orden recomendado de implementación
- Estimación de tiempos
- Tips importantes

### 7. Desglose de Tareas
**Archivo**: `task.md`
- Fases del proyecto completadas
- Checklist de todas las tareas realizadas

### 8. Decisión de Ubicación (Histórico)
**Archivo**: `ANAFI_Location_Decision.md`
- Documento histórico sobre la decisión de ubicación del proyecto

## 🎯 Cómo Usar Esta Documentación

### Para Entender el Sistema
1. Lee primero: `ANAFI_Executive_Summary.md`
2. Luego: `ANAFI_Deep_Agent_Architecture.md`

### Para Implementar
1. Sigue: `ANAFI_Implementation_Guide.md` o `ANAFI_Instructivo_Implementacion.md`
2. Consulta: `ANAFI_Tool_Descriptions.md` cuando implementes cada herramienta

### Para Modificar Comportamiento
1. Revisa: `ANAFI_System_Prompts.md`
2. Edita los prompts en: `src/prompts/`

### Para Agregar Herramientas
1. Consulta: `ANAFI_Tool_Descriptions.md` para ver el patrón
2. Implementa siguiendo los ejemplos en `src/tools/`

## 📊 Estructura del Agente

```
ANAFI_AGENT/
├── documentacion/          # Esta carpeta
├── src/
│   ├── graph/             # Estado y builder
│   ├── models/            # Modelos Pydantic
│   ├── prompts/           # Prompts del sistema
│   ├── agents/            # Configuración de agentes
│   └── tools/             # Implementación de herramientas
├── tests/                 # Tests unitarios
├── requirements.txt       # Dependencias
├── langgraph.json        # Configuración LangGraph
└── .env                  # Variables de entorno
```

## 🚀 Quick Start

1. **Leer documentación**: Empieza con `ANAFI_Executive_Summary.md`
2. **Configurar entorno**: Sigue `ANAFI_Instructivo_Implementacion.md`
3. **Ejecutar agente**: `langgraph dev`
4. **Ejecutar tests**: `pytest tests/ -v`

## 📞 Soporte

Para dudas sobre:
- **Arquitectura**: Consulta `ANAFI_Deep_Agent_Architecture.md`
- **Herramientas**: Consulta `ANAFI_Tool_Descriptions.md`
- **Prompts**: Consulta `ANAFI_System_Prompts.md`
- **Implementación**: Consulta `ANAFI_Implementation_Guide.md`

---

**Nota**: Toda esta documentación fue generada automáticamente y está sincronizada con la implementación actual del agente.
