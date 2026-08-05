from dataclasses import dataclass, field
from typing import Any

from typetemp.environment.typed_environment import TypedEnvironment
from typetemp.environment.typed_native_environment import TypedNativeEnvironment
from typetemp.template.render_mixin import RenderMixin

_env = TypedEnvironment()
_native_env = TypedNativeEnvironment()


@dataclass
class TypedTemplate(RenderMixin):
    """Base typed template with inherited dataclass configuration."""

    source: str | None = None
    use_native: bool = False
    to: str | None = None
    output: Any = field(init=False, default=None)
    env: Any = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        declared_source = type(self).__dict__.get("source")
        if self.source is None and isinstance(declared_source, str):
            self.source = declared_source
        if self.source is None:
            raise ValueError(f"{type(self).__name__} requires a template source")
        self.env = _native_env if self.use_native else _env

    def render(self, **kwargs) -> Any:
        return self._render(**kwargs)

    def __call__(self, **kwargs) -> Any:
        return self.render(**kwargs)
