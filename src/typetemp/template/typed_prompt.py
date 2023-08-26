import inspect
import os
from _ast import stmt
from ast import parse
from dataclasses import is_dataclass, dataclass
from typing import TypeVar, List

from typetemp.environment.typed_environment import TypedEnvironment
from typetemp.environment.typed_native_environment import TypedNativeEnvironment
from typetemp.functional import render_function

_env = TypedEnvironment()
_native_env = TypedNativeEnvironment()


@dataclass
class TypedTemplate:
    """
    Base class for creating templated classes. Uses the jinja2 templating engine
    to render templates. Allows for usage of macros and filters.
    """

    source: str = None  # The string template to be rendered
    use_native: bool = False  # Whether to use NativeEnvironment for rendering
    to: str = None  # The "to" property for rendering destination
    output: str = None  # The rendered output

    def __post_init__(self):
        """
        After the instance is initialized, set the environment
        """
        # Use NativeEnvironment when use_native is True, else use default Environment
        self.env = _native_env if self.use_native else _env

    def __call__(self, **kwargs):
        self.render(**kwargs)

    def render(self, **kwargs) -> str:
        """
        Render the template. Excludes instance variables that
        are not callable (i.e., methods) and don't start with "__".
        """
        template = self.env.from_string(self.__class__.source)

        render_dict = {**self._render_vars(), **kwargs}

        self.output = template.render(**render_dict)

        # Render the "to" property if it's defined
        if self.to:
            to_template = _env.from_string(self.to)
            rendered_to = os.path.join(to_template.render(**render_dict))

            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(rendered_to), exist_ok=True)

            with open(rendered_to, "w") as file:
                file.write(self.output)

        return self.output

    def _render_vars(self):
        """
        Get the instance variables (not including methods or dunder methods)
        """
        properties = {
            name: getattr(self, name)
            for name, value in inspect.getmembers(self)
            if not name.startswith("__") and not callable(value)
        }
        # If the value of a property is a TypedTemplate, render it
        for name, value in properties.items():
            if isinstance(value, TypedTemplate):
                properties[name] = value.render()
        return properties

    def to_function(self, **kwargs) -> stmt:
        """
        Renders the function template and returns its AST object.

        :param kwargs: The keyword arguments to be used in rendering
        :return: The AST object of the rendered function
        """
        rendered_func = self.render(**kwargs)
        return parse(rendered_func).body[0]

    def render_class(self, func_tmpls: List[str] = None, **kwargs):
        """
        Renders the class template and returns the compiled class, optionally including methods.

        :param func_tmpls: A list of template strings for functions to be included in the class
        :param kwargs: The keyword arguments to be used in rendering
        :return: The compiled class
        """
        # Render the class
        rendered_cls = self.render(**kwargs)
        class_ast = parse(rendered_cls)

        # If function templates are provided, render and add them to the class
        if func_tmpls:
            for func_tmpl in func_tmpls:
                function_ast = render_function(func_tmpl, **kwargs)
                class_ast.body[-1].body.append(function_ast)

        # Compile the class AST
        compiled_class_def = compile(class_ast, filename="<ast>", mode="exec")
        class_dict = {}
        exec(compiled_class_def, class_dict)

        # Return the compiled class
        return class_dict[kwargs["class_name"]]
