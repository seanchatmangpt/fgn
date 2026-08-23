from dataclasses import dataclass, field
from typing import List, Optional, Union

from typetemp.template.typed_prompt import TypedPrompt


@dataclass
class TypedCriticalPathTable(TypedPrompt):
    """Generate and normalize a critical-path table as Markdown."""

    title: str | None = None
    columns: List[str] = field(
        default_factory=lambda: ["Step", "Task Description", "Dependencies", "Notes"]
    )
    num_rows: int = 25
    table_md: Optional[str] = field(init=False, default=None)
    source: str = (
        "You are tasked with generating a critical path table. "
        "The project is about {{ user_input }} and should have the following columns: "
        "{{ columns|join(', ') }} and {{ num_rows }} rows."
    )
    sys_msg: str = "You are a critical path table AI assistant."

    def __call__(self, **kwargs) -> Union[str, dict]:
        result = super().__call__(**kwargs)
        if isinstance(result, dict) and isinstance(result.get("steps"), list):
            separator = ["---"] * len(self.columns)
            rows = [self.columns, separator]
            for step in result["steps"]:
                if isinstance(step, dict):
                    rows.append([str(step.get(column, "")) for column in self.columns])
            self.table_md = "\n".join(
                "| " + " | ".join(row) + " |" for row in rows
            )
            self.output = self.table_md
        return self.output


if __name__ == "__main__":
    table_instance = TypedCriticalPathTable(
        columns=["Step", "Task Description", "Dependencies", "Due Date", "Status"],
        num_rows=10,
    )
    table_instance(
        user_input=(
            "I am working on a chiefofstaffgpt.com and need to get the "
            "full stack working with my OpenAI agent"
        ),
        to="stdout",
    )
