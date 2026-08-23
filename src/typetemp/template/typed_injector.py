from __future__ import annotations

import inspect
import os
import re
from dataclasses import is_dataclass
from pathlib import Path

from fgn.core.broker import Broker, Receipt
from typetemp.environment.typed_environment import TypedEnvironment

_env = TypedEnvironment()


class TypedInjector:
    """Render and inject text through the receipt-bound file mutation boundary."""

    source: str | None = None
    to: str | None = None
    before: str | None = None
    after: str | None = None
    at_line: int | None = None
    prepend: bool = False
    append: bool = False
    skip_if: str | None = None
    output: str | None = None
    receipt: Receipt | None = None

    def __init__(self):
        if not is_dataclass(self):
            raise TypeError("TypedInjector classes must be dataclasses.")

    def __post_init__(self) -> None:
        declared_source = type(self).__dict__.get("source")
        if self.source is None and isinstance(declared_source, str):
            self.source = declared_source
        if self.source is None:
            raise ValueError(f"{type(self).__name__} requires an injection source")
        if not self.to:
            raise ValueError(f"{type(self).__name__} requires a target path")
        self.env = _env
        self._broker = Broker()

    def inject(self) -> Receipt | None:
        self.output = self.env.from_string(self.source).render(**self._properties())
        target = Path(self.to)
        content = target.read_text(encoding="utf-8")
        if self.skip_if and re.search(self.skip_if, content):
            return None

        updated = self._updated_content(content)
        if updated == content:
            return None
        self.receipt = self._broker.write_text(target, updated)
        return self.receipt

    def _properties(self):
        return {
            name: getattr(self, name)
            for name, value in inspect.getmembers(self)
            if not name.startswith("__") and not callable(value)
        }

    def _updated_content(self, content: str) -> str:
        assert self.output is not None
        separator = os.linesep
        if self.prepend:
            return self.output + separator + content
        if self.append:
            return content + separator + self.output

        lines = content.splitlines(keepends=True)
        rendered = self.output + separator
        if self.at_line is not None:
            index = max(0, min(self.at_line - 1, len(lines)))
            lines.insert(index, rendered)
            return "".join(lines)
        if self.before is not None:
            for index, line in enumerate(lines):
                if re.search(self.before, line):
                    lines.insert(index, rendered)
                    return "".join(lines)
            return content
        if self.after is not None:
            for index, line in enumerate(lines):
                if re.search(self.after, line):
                    lines.insert(index + 1, rendered)
                    return "".join(lines)
            return content
        raise ValueError("one injection position must be configured")
