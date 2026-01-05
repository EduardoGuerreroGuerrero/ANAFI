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
