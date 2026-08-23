import importlib.util
import sys

import pytest
from click.testing import CliRunner
from jinja2 import Template

from fgn.core.broker import Broker


CLI_TEMPLATE = """
import click

@click.group()
def cli():
    pass

{% for command in commands %}
@click.command(name='{{ command.name }}')
{% for option in command.options %}
@click.option('--{{ option.name }}', type={{ option.type }}, required={{ option.required }})
{% endfor %}
def {{ command.name }}({{ command.args }}):
    click.echo('Command {{ command.name }} executed.')

cli.add_command({{ command.name }})
{% endfor %}
"""

COMMANDS = [
    {"name": "create", "args": "item, value", "options": [
        {"name": "item", "type": "str", "required": "True"},
        {"name": "value", "type": "str", "required": "True"},
    ]},
    {"name": "read", "args": "item", "options": [
        {"name": "item", "type": "str", "required": "True"},
    ]},
    {"name": "update", "args": "item, new_value", "options": [
        {"name": "item", "type": "str", "required": "True"},
        {"name": "new_value", "type": "str", "required": "True"},
    ]},
    {"name": "delete", "args": "item", "options": [
        {"name": "item", "type": "str", "required": "True"},
    ]},
]


@pytest.fixture
def generated_cli(tmp_path):
    module_path = tmp_path / "generated_cli.py"
    receipt = Broker(tmp_path / "receipts").write_text(
        module_path,
        Template(CLI_TEMPLATE).render(commands=COMMANDS),
    )
    assert receipt.status == "ALIVE"

    spec = importlib.util.spec_from_file_location("generated_cli", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    try:
        yield module
    finally:
        sys.modules.pop(spec.name, None)


@pytest.mark.parametrize(
    ("command", "expected_output"),
    [
        ("create --item test --value value", "Command create executed.\n"),
        ("read --item test", "Command read executed.\n"),
        ("update --item test --new_value new_value", "Command update executed.\n"),
        ("delete --item test", "Command delete executed.\n"),
    ],
)
def test_generated_crud_commands(generated_cli, command, expected_output):
    result = CliRunner().invoke(generated_cli.cli, command.split())
    assert result.exit_code == 0, result.output
    assert result.output == expected_output
