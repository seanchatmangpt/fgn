from _ast import stmt
from ast import parse, dump, AST
from typing import List

from typetemp.environment.typed_environment import TypedEnvironment
from typetemp.environment.typed_native_environment import TypedNativeEnvironment

_env = TypedEnvironment()
_native_env = TypedNativeEnvironment()


def render(tmpl_str: str, **kwargs) -> str:
    """
    Render a template string with the given keyword arguments.
    """
    template = _env.from_string(tmpl_str)

    return template.render(**kwargs)


def render_native(tmpl_str: str, **kwargs) -> str:
    """
    Render a template string with the given keyword arguments.
    """
    template = _native_env.from_string(tmpl_str)

    return template.render(**kwargs)


def render_function(func_tmpl: str, **kwargs) -> stmt:
    """
    Renders the function template and returns its AST object.

    :param func_tmpl: The template string of the function
    :param kwargs: The keyword arguments to be used in rendering
    :return: The AST object of the rendered function
    """
    rendered_func = render(func_tmpl, **kwargs)
    return parse(rendered_func).body[0]


def render_class(cls_tmpl: str, func_tmpls: List[str] = None, **kwargs):
    """
    Renders the class template and returns the compiled class, optionally including methods.

    :param cls_tmpl: The template string of the class
    :param func_tmpls: A list of template strings for functions to be included in the class
    :param use_dataclass: Whether to decorate the class with the @dataclass decorator
    :param kwargs: The keyword arguments to be used in rendering
    :return: The compiled class
    """
    # Render the class
    rendered_cls = render(cls_tmpl, **kwargs)
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
