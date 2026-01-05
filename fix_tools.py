"""Script to fix import errors in tool files"""
import re
from pathlib import Path

def fix_tool_file(filepath):
    """Remove InjectedState imports and simplify function signatures"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove problematic imports
    content = re.sub(r'from langchain_core\.tools import InjectedState, InjectedToolCallId\n', '', content)
    content = re.sub(r'from src\.graph\.state import DeepAgentState\n', '', content)
    content = re.sub(r'from typing import Annotated,', 'from typing import', content)
    content = re.sub(r'import json\n', '', content, count=1)  # Remove first json import if not needed
    
    # Simplify function signatures - remove state parameters
    content = re.sub(
        r'(\w+)\(\s*([^)]*?),?\s*state: Annotated\[DeepAgentState, InjectedState\],\s*tool_call_id: Annotated\[str, InjectedToolCallId\],',
        r'\1(\2, data: dict,',
        content
    )
    
    # Remove .description assignments
    content = re.sub(r'\n\n\w+\.description = """[^"]+"""\n', '\n', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed {filepath.name}")

# Fix the two remaining files
fix_tool_file(Path('src/tools/scenario_analysis_tools.py'))
fix_tool_file(Path('src/tools/report_generation_tools.py'))
print("Done!")
