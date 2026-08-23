from unittest.mock import MagicMock

import pytest

from fgn.core.broker import Broker, Receipt
from fgn.utils.output_manager import OutputManager


def receipt(action: str) -> Receipt:
    return Receipt(
        receipt_id=f"receipt-{action}",
        intent_id=f"intent-{action}",
        action=action,
        subject="test",
        status="ALIVE",
        phase="verified",
        started_at="2026-08-05T00:00:00Z",
        completed_at="2026-08-05T00:00:01Z",
    )


@pytest.fixture
def broker():
    value = MagicMock(spec=Broker)
    value.copy_text.return_value = receipt("clipboard.copy")
    value.write_text.return_value = receipt("file.write")
    return value


@pytest.fixture
def output_manager(broker):
    return OutputManager(broker=broker)


def test_handle_output_no_flags_copies_only(broker, output_manager):
    result = output_manager.handle_output("Test response")
    broker.copy_text.assert_called_once_with("Test response")
    broker.write_text.assert_not_called()
    assert [item.action for item in result] == ["clipboard.copy"]


def test_handle_output_output_flag_writes_and_copies(broker, output_manager):
    output_manager.output = "test_output.md"
    result = output_manager.handle_output("Test response")
    broker.write_text.assert_called_once_with(
        "test_output.md", "Test response", append=False
    )
    broker.copy_text.assert_called_once_with("Test response")
    assert [item.action for item in result] == ["file.write", "clipboard.copy"]


def test_handle_output_auto_output_flag_writes_generated_target(broker, output_manager):
    output_manager.auto_output = True
    result = output_manager.handle_output("Test response")
    target, content = broker.write_text.call_args.args
    assert target.endswith(".md")
    assert content == "Test response"
    assert broker.write_text.call_args.kwargs == {"append": False}
    assert [item.action for item in result] == ["file.write", "clipboard.copy"]


def test_handle_output_no_copy_flag_has_no_actuation(broker, output_manager):
    output_manager.no_copy = True
    assert output_manager.handle_output("Test response") == []
    broker.copy_text.assert_not_called()
    broker.write_text.assert_not_called()


def test_save_to_file_generated_filename_is_receipted(broker, output_manager):
    result = output_manager.save_to_file("Test response")
    target, content = broker.write_text.call_args.args
    assert target.endswith(".md")
    assert content == "Test response"
    assert result.action == "file.write"


def test_save_to_file_with_filename_is_receipted(broker, output_manager):
    result = output_manager.save_to_file("Test response", "test_output.md")
    broker.write_text.assert_called_once_with(
        "test_output.md", "Test response", append=False
    )
    assert result.action == "file.write"


def test_save_to_file_append_preserves_separator(broker, output_manager):
    output_manager.save_to_file("Test response", "test_output.md", append=True)
    broker.write_text.assert_called_once_with(
        "test_output.md", "\n\nTest response", append=True
    )
