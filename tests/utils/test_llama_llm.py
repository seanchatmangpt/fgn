from types import SimpleNamespace
from unittest.mock import MagicMock

from fgn.core.broker import Receipt
from fgn.utils.llama_llm import LocalLlamaClient


def test_local_llama_executes_through_broker():
    broker = MagicMock()
    receipt = Receipt(
        receipt_id="r1",
        intent_id="i1",
        action="process.shell",
        subject="/tmp/llama",
        status="ALIVE",
        phase="verified",
        started_at="2026-08-05T00:00:00Z",
    )
    broker.run_shell.return_value = (
        SimpleNamespace(returncode=0, stdout="model output\n", stderr=""),
        receipt,
    )
    client = LocalLlamaClient(llama_home="/tmp/llama", broker=broker)

    assert client.complete(prompt="hello") == "model output"
    command = broker.run_shell.call_args.args[0]
    assert "/tmp/llama/main" in command
    assert "hello" in command
    assert broker.run_shell.call_args.kwargs == {"admitted": True, "cwd": "/tmp/llama"}
    assert client.last_receipt is receipt
