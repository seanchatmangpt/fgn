from dataclasses import dataclass, field
from typing import Any, Callable, Union

from fgn.completion.chat import chat
from typetemp.environment.typed_environment import TypedEnvironment
from typetemp.environment.typed_native_environment import TypedNativeEnvironment
from typetemp.template.render_mixin import RenderMixin

_env = TypedEnvironment()
_native_env = TypedNativeEnvironment()


@dataclass
class TypedPrompt(RenderMixin):
    """Render a typed prompt and execute it through an injectable chat boundary."""

    source: str | None = None
    user_input: str | None = None
    output: Union[str, dict, None] = field(init=False, default=None)
    sys_msg: str = "You are a prompt AI assistant."
    model: str = "3i"
    to: str | None = None
    use_native: bool = False
    chat_inst: Callable[..., Union[str, dict]] = field(
        default=chat,
        repr=False,
        compare=False,
    )
    env: Any = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        declared_source = type(self).__dict__.get("source")
        if self.source is None and isinstance(declared_source, str):
            self.source = declared_source
        if self.source is None:
            raise ValueError(f"{type(self).__name__} requires a prompt source")
        self.env = _native_env if self.use_native else _env

    def __call__(self, **kwargs) -> Union[str, dict]:
        rendered_prompt = self._render(**kwargs)
        self.output = self.chat_inst(
            prompt=rendered_prompt,
            sys_msg=self.sys_msg,
            model=self.model,
        )
        return self.output


if __name__ == "__main__":
    typed_prompt = TypedPrompt(
        source="Hello {{ name }}! How are you doing today?",
        to="stdout",
    )
    user_input = typed_prompt(name="John Doe")
    print(f"User input: {user_input}")
