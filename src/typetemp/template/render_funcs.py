from typing import Any

from typetemp.environment.typed_environment import TypedEnvironment
from typetemp.environment.typed_native_environment import TypedNativeEnvironment

_env = TypedEnvironment()
_native_env = TypedNativeEnvironment()


def render_str(source, env=_env, **kwargs) -> str:
    template = env.from_string(source)

    return template.render(**kwargs)


def render_py(source, env=_native_env, **kwargs) -> Any:
    template = env.from_string(source)

    return template.render(**kwargs)