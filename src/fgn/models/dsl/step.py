from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Step:
    action: str
    description: Optional[str] = None
    run: Optional[str] = None
    command: Optional[str] = None
    options: Optional[Dict[str, str]] = None
    file_path: Optional[str] = None
    name: Optional[str] = None
    value: Optional[str] = None
