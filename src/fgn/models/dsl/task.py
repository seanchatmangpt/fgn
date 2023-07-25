from dataclasses import dataclass, field
from typing import List, Optional

from fgn.models.dsl.step import Step


@dataclass
class Task:
    name: str
    description: Optional[str] = None
    steps: List[Step] = field(default_factory=list)
