from typing import Dict, Any
import os
import inspect


class RenderMixin:
    """
    A mixin class that encapsulates the render and _render_vars functionality.
    This class checks for the required properties 'source', 'env', 'to', and 'output'.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _render(self, **kwargs) -> str:
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
            os.makedirs(os.path.dirname(rendered_to), exist_ok=True)

            with open(rendered_to, "w") as file:
                file.write(self.output)

        return self.output

    def _render_vars(self) -> Dict[str, Any]:
        """
        Get the instance variables (not including methods or dunder methods).
        """
        properties = {
            name: getattr(self, name)
            for name, value in inspect.getmembers(self)
            if not name.startswith("__") and not callable(value)
        }

        # If the value of a property is a TypedTemplate, render it
        for name, value in properties.items():
            if isinstance(value, RenderMixin):
                properties[name] = value.render()

        return properties
