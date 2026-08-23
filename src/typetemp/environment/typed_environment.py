from jinja2 import Environment

from typetemp.extension.faker_extension import FakerExtension
from typetemp.extension.inflection_extension import InflectionExtension


class TypedEnvironment(Environment):
    def __init__(self, **kwargs):
        super().__init__(trim_blocks=True, lstrip_blocks=True, **kwargs)
        self.add_extension(FakerExtension)
        self.add_extension(InflectionExtension)
        try:
            self.add_extension("jinja2_time.TimeExtension")
        except ImportError:
            pass
        self.add_extension("jinja2.ext.i18n")
        self.add_extension("jinja2.ext.debug")
        self.add_extension("jinja2.ext.do")
        self.add_extension("jinja2.ext.loopcontrols")
