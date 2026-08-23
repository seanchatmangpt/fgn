import os
from typing import Any, Dict

from fgn.core.broker import Broker
from typetemp.template.render_funcs import render_str


class RenderMixin:
    """Shared deterministic rendering with receipt-bound output actuation."""

    def _render(self, **kwargs) -> Any:
        template = self.env.from_string(self.source)
        render_dict = {**self._render_vars(), **kwargs}
        self.output = template.render(**render_dict)

        if self.to == "stdout":
            print(self.output)
        elif self.to:
            to_template = self.env.from_string(self.to)
            rendered_to = os.path.join(to_template.render(**render_dict))
            Broker().write_text(rendered_to, str(self.output))

        return self.output

    def _render_vars(self) -> Dict[str, Any]:
        properties = self.__dict__.copy()
        for name, value in properties.items():
            if isinstance(value, RenderMixin):
                properties[name] = value._render()
            elif isinstance(value, str):
                properties[name] = render_str(value)
        return properties
