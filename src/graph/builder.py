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
