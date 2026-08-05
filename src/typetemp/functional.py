from _ast import stmt
from ast import parse, unparse
from typing import List

from fgn.core.broker import Broker, Receipt
from typetemp.environment.typed_environment import TypedEnvironment
from typetemp.environment.typed_native_environment import TypedNativeEnvironment

_env = TypedEnvironment()
_native_env = TypedNativeEnvironment()


def render(tmpl_str: str, **kwargs) -> str:
    return _env.from_string(tmpl_str).render(**kwargs)


def render_native(tmpl_str: str, **kwargs):
    return _native_env.from_string(tmpl_str).render(**kwargs)


def render_function(func_tmpl: str, **kwargs) -> stmt:
    return parse(render(func_tmpl, **kwargs)).body[0]


def render_class(
    cls_tmpl: str,
    func_tmpls: List[str] | None = None,
    *,
    admitted: bool = False,
    broker: Broker | None = None,
    **kwargs,
):
    """Render a class and execute it only through explicitly admitted BRCE."""
    class_ast = parse(render(cls_tmpl, **kwargs))
    if func_tmpls:
        for func_tmpl in func_tmpls:
            class_ast.body[-1].body.append(render_function(func_tmpl, **kwargs))
    source = unparse(class_ast) + "\n"
    namespace, receipt = (broker or Broker()).execute_python(
        source,
        admitted=admitted,
        filename="<typetemp.render_class>",
    )
    rendered_class = namespace[kwargs["class_name"]]
    setattr(rendered_class, "__fgn_receipt__", receipt)
    return rendered_class
