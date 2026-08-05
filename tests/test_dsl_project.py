import json
import shlex
import sys

import pytest

from fgn.core.broker import ActuationRefused
from fgn.core.command_context import CommandContext
from fgn.core.dsl_parser import process_schema
from fgn.models.dsl.fgn_dsl_schema import FgnDslSchema
from fgn.models.dsl.step import Step
from fgn.models.dsl.task import Task


def _schema(command: str) -> FgnDslSchema:
    return FgnDslSchema(
        version="1",
        tasks=[Task(name="shell-boundary", steps=[Step(action="shell", run=command)])],
    )


def test_dsl_shell_is_refused_without_explicit_admission(monkeypatch, tmp_path):
    receipts = tmp_path / "receipts"
    monkeypatch.setenv("FGN_RECEIPT_DIR", str(receipts))
    monkeypatch.delenv("FGN_ALLOW_DSL_SHELL", raising=False)

    with pytest.raises(ActuationRefused) as raised:
        process_schema(_schema("echo forbidden"), CommandContext())

    assert raised.value.receipt.status == "REFUSED:SHELL_AUTHORITY_REQUIRED"
    receipt = json.loads(next(receipts.glob("*.json")).read_text(encoding="utf-8"))
    assert receipt["action"] == "process.shell"
    assert receipt["phase"] == "observed-failure"


def test_dsl_shell_executes_only_through_broker(monkeypatch, tmp_path):
    receipts = tmp_path / "receipts"
    output = tmp_path / "dsl-output.txt"
    monkeypatch.setenv("FGN_RECEIPT_DIR", str(receipts))
    monkeypatch.setenv("FGN_ALLOW_DSL_SHELL", "1")
    command = (
        f"{shlex.quote(sys.executable)} -c "
        + shlex.quote(f"from pathlib import Path; Path({str(output)!r}).write_text('alive')")
    )

    process_schema(_schema(command), CommandContext())

    assert output.read_text(encoding="utf-8") == "alive"
    receipt = json.loads(next(receipts.glob("*.json")).read_text(encoding="utf-8"))
    assert receipt["action"] == "process.shell"
    assert receipt["status"] == "ALIVE"
    assert receipt["consequence"]["exit_code"] == 0
