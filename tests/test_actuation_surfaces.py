from pathlib import Path
from fgn.core.broker import Broker
from fgn.core.commands.template.template_cmd import create_command_scaffold
from typetemp.template.dsl_project import load_yaml_dsl, write_default_chain
from typetemp.utils import create_init_files


def test_command_scaffold_is_fully_receipted(tmp_path):
    broker = Broker(receipt_dir=tmp_path / "receipts")
    receipts = create_command_scaffold("audit", command_root=tmp_path / "commands", broker=broker)
    assert len(receipts) == 7
    assert all(receipt.status == "ALIVE" for receipt in receipts)
    assert (tmp_path / "commands/audit/audit_cmd.py").exists()


def test_default_chain_export_is_explicit_and_receipted(tmp_path):
    target = tmp_path / "chain.yaml"
    receipt = write_default_chain(target, broker=Broker(receipt_dir=tmp_path / "receipts"))
    assert receipt.status == "ALIVE"
    assert "TypedRequirementAnalysisPrompt" in load_yaml_dsl(target)


def test_create_init_files_only_mutates_missing_markers(tmp_path, monkeypatch):
    monkeypatch.setenv("FGN_RECEIPT_DIR", str(tmp_path / "receipts"))
    nested = tmp_path / "a/b"
    nested.mkdir(parents=True)
    receipts = create_init_files(tmp_path)
    assert len(receipts) == 3
    assert all(receipt.status == "ALIVE" for receipt in receipts)
    assert all(path.exists() for path in (tmp_path / "__init__.py", tmp_path / "a/__init__.py", nested / "__init__.py"))
    assert create_init_files(tmp_path) == []
