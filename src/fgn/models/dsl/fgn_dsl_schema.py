from dataclasses import dataclass, field
from typing import Optional, List

from fgn.models.dsl.task import Task


@dataclass
class FgnDslSchema:
    version: Optional[str] = None
    description: Optional[str] = None
    tasks: List[Task] = field(default_factory=list)
