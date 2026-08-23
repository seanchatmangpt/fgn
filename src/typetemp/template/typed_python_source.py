from _ast import stmt
from ast import parse, unparse
from dataclasses import dataclass
from typing import List

from fgn.core.broker import Broker
from typetemp.environment.typed_environment import TypedEnvironment
from typetemp.environment.typed_native_environment import TypedNativeEnvironment
from typetemp.functional import render_function as render_func
from typetemp.template.render_mixin import RenderMixin

_env = TypedEnvironment()
_native_env = TypedNativeEnvironment()


@dataclass
class TypedPythonSource(RenderMixin):
    source: str | None = None
    use_native: bool = False
    to: str | None = None
    output: str | None = None

    def __post_init__(self):
        declared_source = type(self).__dict__.get("source")
        if self.source is None and isinstance(declared_source, str):
            self.source = declared_source
        if self.source is None:
            raise ValueError(f"{type(self).__name__} requires a Python source template")
        self.env = _native_env if self.use_native else _env

    def __call__(self, **kwargs) -> str:
        return self._render(**kwargs)

    def render_function(self, **kwargs) -> stmt:
        return parse(self._render(**kwargs)).body[0]

    def render_class(
        self,
        func_tmpls: List[str] | None = None,
        *,
        admitted: bool = False,
        broker: Broker | None = None,
        **kwargs,
    ):
        class_ast = parse(self._render(**kwargs))
        if func_tmpls:
            for func_tmpl in func_tmpls:
                class_ast.body[-1].body.append(render_func(func_tmpl, **kwargs))
        source = unparse(class_ast) + "\n"
        namespace, receipt = (broker or Broker()).execute_python(
            source,
            admitted=admitted,
            filename=f"<{type(self).__name__}.render_class>",
        )
        rendered_class = namespace[kwargs["class_name"]]
        setattr(rendered_class, "__fgn_receipt__", receipt)
        return rendered_class
