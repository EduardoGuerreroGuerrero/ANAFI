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
