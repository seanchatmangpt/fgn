from dataclasses import dataclass, field
from typing import List, Optional

from typetemp.template.typed_prompt import TypedPrompt


@dataclass
class TypedCriticalPathTable(TypedPrompt):
    """
    Class that creates a critical path table dynamically.
    It uses Chat capabilities for dynamic table creation.
    """
    title: str = None  # Title or description of the project
    columns: List[str] = field(default_factory=lambda: ["Step", "Task Description", "Dependencies", "Notes"])
    num_rows: int = 25  # Number of rows in the table
    table_md: Optional[str] = field(init=False, default=None)  # The Markdown table
    source: str = "You are tasked with generating a critical path table. " \
                  "The project is about {{ user_input }} and should have the following columns: " \
                  "{{ columns|join(', ') }} and {{ num_rows }} rows."
    sys_msg: str = "You are a critical path table AI assistant."


if __name__ == "__main__":
    table_instance = TypedCriticalPathTable(
        user_input="I am working on a chiefofstaffgpt.com and need to get the full stack working"
                   "with my OpenAI agent",
        columns=["Step", "Task Description", "Dependencies", "Due Date", "Status"],
        num_rows=10,
        to="stdout"
    )()
