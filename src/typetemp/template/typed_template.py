from dataclasses import  dataclass

from typetemp.environment.typed_environment import TypedEnvironment
from typetemp.environment.typed_native_environment import TypedNativeEnvironment
from typetemp.template.render_mixin import RenderMixin

_env = TypedEnvironment()
_native_env = TypedNativeEnvironment()


class TypedTemplate(RenderMixin):
    """
    Base class for creating templated classes. Uses the jinja2 templating engine
    to render templates. Allows for usage of macros and filters.
    """
    source: str = None  # The string template to be rendered
    use_native: bool = False  # Whether to use NativeEnvironment for rendering
    to: str = None  # The "to" property for rendering destination
    output: str = None  # The rendered output

    def __init__(self, **kwargs):
        self.__post_init__()
        self.__dict__.update(kwargs)

    def __post_init__(self):
        """
        After the instance is initialized, set the environment
        """
        # Use NativeEnvironment when use_native is True, else use default Environment
        self.env = _native_env if self.use_native else _env

    def __call__(self, **kwargs) -> str:
        return self._render(**kwargs)
