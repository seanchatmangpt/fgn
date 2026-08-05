import json

from click.testing import CliRunner

from fgn.cli import main
from fgn.core.broker import ActuationRefused, Broker


def test_file_writer_emits_verified_receipt(tmp_path):
    runner = CliRunner()
    output = tmp_path / "message.txt"
    receipts = tmp_path / "receipts"

    result = runner.invoke(main, ["--receipt-dir", str(receipts), "-o", str(output), "Hello World!"])

    assert result.exit_code == 0, result.output
    assert result.output.strip() == "Hello World!"
    assert output.read_text(encoding="utf-8") == "Hello World!"

    receipt_files = list(receipts.glob("*.json"))
    assert len(receipt_files) == 1
    receipt = json.loads(receipt_files[0].read_text(encoding="utf-8"))
    assert receipt["action"] == "file.write"
    assert receipt["status"] == "ALIVE"
    assert receipt["phase"] == "verified"
    assert receipt["subject"] == str(output.absolute())
    assert receipt["input_sha256"] == receipt["output_sha256"]


def test_append_is_atomic_and_receipted(tmp_path):
    receipts = tmp_path / "receipts"
    output = tmp_path / "append.txt"
    broker = Broker(receipts)

    first = broker.write_text(output, "one")
    second = broker.write_text(output, "two", append=True)

    assert output.read_text(encoding="utf-8") == "onetwo"
    assert first.status == "ALIVE"
    assert second.status == "ALIVE"
    assert len(list(receipts.glob("*.json"))) == 2


def test_shell_requires_explicit_admission(tmp_path):
    broker = Broker(tmp_path / "receipts")
    try:
        broker.run_shell("echo refused")
    except ActuationRefused as error:
        assert error.receipt.status == "REFUSED:SHELL_AUTHORITY_REQUIRED"
    else:
        raise AssertionError("shell execution was not refused")
