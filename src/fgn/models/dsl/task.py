from dataclasses import dataclass, field
from typing import Optional, List

from fgn.models.dsl.step import Step


@dataclass
class Task:
    name: str
    description: Optional[str] = None
    steps: List[Step] = field(default_factory=list)
