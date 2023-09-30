from typing import Dict, Any
import os
import inspect

from typetemp.template.render_funcs import render_str


class RenderMixin:
    """
    A mixin class that encapsulates the render and _render_vars functionality.
    This class checks for the required properties 'source', 'env', 'to', and 'output'.
    """
    def _render(self, **kwargs) -> Any:
        """
        Render the template. Excludes instance variables that
        are not callable (i.e., methods) and don't start with "__".
        """
        template = self.env.from_string(self.source)

        render_dict = {**self._render_vars(), **kwargs}

        self.output = template.render(**render_dict)

        # Render the "to" property if it's defined
        if self.to == "stdout":
            print(self.output)
        elif self.to:
            to_template = self.env.from_string(self.to)
            rendered_to = os.path.join(to_template.render(**render_dict))

            # Create the directory if it doesn't exist
            # os.makedirs(os.path.dirname(rendered_to), exist_ok=True)

            with open(rendered_to, "w") as file:
                file.write(self.output)

        return self.output

    def _render_vars(self) -> Dict[str, Any]:
        """
        Get the instance variables (not including methods or dunder methods).
        """
        # copy the self dict
        properties = self.__dict__.copy()

        # If the value of a property is a TypedTemplate, render it
        for name, value in properties.items():
            if isinstance(value, RenderMixin):
                properties[name] = value._render()
            elif isinstance(value, str):
                properties[name] = render_str(value)

        return properties
