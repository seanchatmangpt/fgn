from collections import namedtuple
from dataclasses import dataclass

import pytest
from faker import Faker

from typetemp.template.typed_injector import TypedInjector
from typetemp.template.typed_template import TypedTemplate


@dataclass
class ComplexMultiLineTemplate(TypedTemplate):
    class_name: str = None
    attributes: list = None
    methods: list = None

    source = """class {{ class_name }}:
    def __init__(self{% for attr in attributes %}, {{ attr.name }}: {{ attr.type }}{% endfor %}):
        {% for attr in attributes -%}
        self.{{ attr.name }} = {{ attr.name }}
        {% endfor %}
    {%- for method in methods %}
    def {{ method.name }}(self{% for param in method.params %}, {{ param.name }}: {{ param.type }}{% endfor %}):
        return "{{ faker_sentence() }}"  # Simulating logic with Faker sentence{% endfor %}"""


@pytest.fixture
def rendered_complex_multiline_template():
    faker = Faker()
    Attribute = namedtuple("Attribute", ["name", "type"])
    Method = namedtuple("Method", ["name", "params"])
    Param = namedtuple("Param", ["name", "type"])
    attributes = [Attribute(name=faker.word(), type=faker.word()) for _ in range(3)]
    methods = [
        Method(name=faker.word(), params=[Param(name=faker.word(), type=faker.word()) for _ in range(2)])
        for _ in range(3)
    ]
    return ComplexMultiLineTemplate(
        class_name=faker.word().capitalize(), attributes=attributes, methods=methods
    ).render()


@pytest.fixture
def target_path(tmp_path, rendered_complex_multiline_template, monkeypatch):
    monkeypatch.setenv("FGN_RECEIPT_DIR", str(tmp_path / "receipts"))
    target = tmp_path / "target.py"
    target.write_text(rendered_complex_multiline_template)
    return target


@dataclass
class AfterInjectHelloWorld(TypedInjector):
    place: str
    to: str
    source = "    Hello {{ place }}!"
    after = "__init__"


def test_inject_after_init_method(target_path):
    injector = AfterInjectHelloWorld(to=str(target_path), place="World")
    receipt = injector.inject()
    assert target_path.read_text().split("\n")[2] == injector.output
    assert receipt.status == "ALIVE"


@dataclass
class BeforeInjectHelloWorld(TypedInjector):
    place: str
    to: str
    source = '    """Hello {{ place }}!"""'
    before = "__init__"


def test_inject_before_init_method(target_path):
    injector = BeforeInjectHelloWorld(to=str(target_path), place="World")
    receipt = injector.inject()
    assert target_path.read_text().split("\n")[1] == injector.output
    assert receipt.status == "ALIVE"


@dataclass
class AtInjectHelloWorld(TypedInjector):
    place: str
    to: str
    source = """    def {{ place }}():
        return 'hello {{ place }}!'"""
    at_line = 6


def test_inject_at_line(target_path):
    injector = AtInjectHelloWorld(to=str(target_path), place="World")
    receipt = injector.inject()
    inj_lines = injector.output.split("\n")
    lines = target_path.read_text().splitlines(keepends=True)
    assert lines[injector.at_line - 1] == inj_lines[0] + "\n"
    assert lines[injector.at_line] == inj_lines[1] + "\n"
    assert receipt.status == "ALIVE"


@dataclass
class SkipInjectHelloWorld(TypedInjector):
    place: str
    to: str
    source = "    Hello {{ place }}!"
    before = "__init__"
    skip_if = "__init__"


def test_inject_skip_if_exists(target_path):
    original = target_path.read_text()
    injector = SkipInjectHelloWorld(to=str(target_path), place="World")
    assert injector.inject() is None
    assert target_path.read_text() == original


@dataclass
class PrependInjectHelloWorld(TypedInjector):
    place: str
    to: str
    source = "from hello import {{ place }}"
    prepend = True


def test_inject_prepend(target_path):
    injector = PrependInjectHelloWorld(to=str(target_path), place="World")
    receipt = injector.inject()
    assert target_path.read_text().split("\n")[0] == injector.output
    assert receipt.status == "ALIVE"


@dataclass
class AppendInjectHelloWorld(TypedInjector):
    place: str
    to: str
    source = """def {{ place }}():
    return 'hello {{ place }}!'"""
    append = True


def test_inject_append(target_path):
    injector = AppendInjectHelloWorld(to=str(target_path), place="world")
    receipt = injector.inject()
    lines = target_path.read_text().split("\n")
    inj_lines = injector.output.split("\n")
    assert lines[-2:] == inj_lines
    assert receipt.status == "ALIVE"
