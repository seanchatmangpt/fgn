from dataclasses import dataclass, field
from typing import Union

from fgn.completion.chat import Chat
from typetemp.environment.typed_environment import TypedEnvironment
from typetemp.environment.typed_native_environment import TypedNativeEnvironment
from typetemp.template.typed_template import TypedTemplate

_env = TypedEnvironment()
_native_env = TypedNativeEnvironment()


@dataclass
class TypedPrompt(TypedTemplate):
    """
    Class that incorporates the TypedPrompt functionality along with the Chat class.
    It first renders the prompt using the mixin render method and then passes it to the chat function.
    """
    user_input: str = None
    chat_inst: Chat = field(default_factory=Chat)  # An instance of the Chat class
    output: Union[str, dict] = None  # The response from the chat function
    sys_msg: str = "You are a prompt AI assistant."
    model: str = "3"

    def __call__(self, **kwargs) -> Union[str, dict]:
        # First, use mixin's render function to get the rendered output
        rendered_prompt = self._render(**kwargs)

        self.output = self.chat_inst(prompt=rendered_prompt, sys_msg=self.sys_msg, model=self.model)
        # Pass the rendered prompt to the chat function

        if self.to == "stdout":
            print(self.output)

        return self.output


if __name__ == "__main__":
    # Create an instance of the TypedPrompt class
    typed_prompt = TypedPrompt(source="Hello {{ name }}! How are you doing today?",
                               to="stdout")

    # Render the prompt and get the user input
    user_input = typed_prompt(name="John Doe")

    print(f"User input: {user_input}")
