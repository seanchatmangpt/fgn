from pathlib import Path

from fgn.core.broker import Broker
from utils.peq import Peq


def test_initializes_missing_module_with_receipt(tmp_path):
    target = tmp_path / "sample_module.py"
    broker = Broker(receipt_dir=tmp_path / "receipts")
    peq = Peq(target, broker=broker)
    assert target.exists()
    assert peq.module is not None
    assert peq.receipts[-1].status == "ALIVE"


def test_loads_existing_module(tmp_path):
    target = tmp_path / "hello_module.py"
    target.write_text("def hello():\n    return 'Hello, World!'\n")
    peq = Peq(target, broker=Broker(receipt_dir=tmp_path / "receipts"))
    assert peq.hello() == "Hello, World!"


def test_callable_assignment_persists_and_reloads(tmp_path):
    target = tmp_path / "sample_module.py"
    peq = Peq(target, broker=Broker(receipt_dir=tmp_path / "receipts"))

    def greet():
        return "Hello, World!"

    peq.greet = greet
    assert peq.greet() == "Hello, World!"
    assert "def greet" in target.read_text()


def test_undo_and_redo_restore_exact_states(tmp_path):
    target = tmp_path / "sample_module.py"
    peq = Peq(target, broker=Broker(receipt_dir=tmp_path / "receipts"))
    peq.answer = 42
    assert peq.answer == 42
    assert peq.undo()
    assert not hasattr(peq.module, "answer")
    assert peq.redo()
    assert peq.answer == 42


def test_duplicate_import_is_not_added(tmp_path):
    target = tmp_path / "sample_module.py"
    peq = Peq(target, broker=Broker(receipt_dir=tmp_path / "receipts"))
    peq.add_import("import os")
    peq.add_import("import os")
    assert target.read_text().count("import os") == 1
