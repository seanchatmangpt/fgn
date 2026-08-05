import json
from types import SimpleNamespace

import pytest

from fgn.core.chat_agent import ChatAgent
from fgn.models.message import Message
from fgn.utils.llm_operations import (
    LLMProviderError,
    chat,
    generate_filename,
    gpt_chat_completion,
)


class FakeCompletions:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return self.response


class FakeClient:
    def __init__(self, response):
        self.completions = FakeCompletions(response)
        self.chat = SimpleNamespace(completions=self.completions)


def response_with(content="success", function_call=None):
    message = SimpleNamespace(content=content, function_call=function_call)
    return SimpleNamespace(choices=[SimpleNamespace(message=message)])


def test_import_and_missing_key_are_typed(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(LLMProviderError) as raised:
        gpt_chat_completion([{"role": "user", "content": "hello"}], model="test")
    assert raised.value.code == "OPENAI_API_KEY_MISSING"


def test_injected_client_executes_without_openai_package(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))
    client = FakeClient(response_with("success"))
    result = gpt_chat_completion(
        [{"role": "user", "content": "hello"}],
        model="test-model",
        client=client,
    )
    assert result == "success"
    assert client.completions.calls[0]["model"] == "test-model"
    receipt_files = list((tmp_path / ".fgn" / "receipts").glob("*.json"))
    assert receipt_files
    assert json.loads(receipt_files[0].read_text())["status"] == "ALIVE"


def test_function_call_arguments_are_decoded():
    function_call = {"name": "change_value", "arguments": '{"key":"top","value":10}'}
    client = FakeClient(response_with(function_call=function_call))
    result = chat("change", funcs=[{"name": "change_value"}], client=client)
    assert result == {"name": "change_value", "arguments": {"key": "top", "value": 10}}


def test_filename_generation_is_deterministic_and_offline():
    first = generate_filename("A Durable Receipt-Bound File", time=False)
    second = generate_filename("A Durable Receipt-Bound File", time=False)
    assert first == second == "a_durable_receipt_bound_file.md"


def test_chat_agent_history_is_persisted_through_broker(monkeypatch, tmp_path):
    monkeypatch.setenv("FGN_RECEIPT_DIR", str(tmp_path / "receipts"))
    history = tmp_path / "history.json"
    agent = ChatAgent(model="test", history_path=str(history), messages=[Message("user", "hello")])
    receipt = agent.save()
    assert receipt.status == "ALIVE"
    assert json.loads(history.read_text())["messages"] == [{"role": "user", "content": "hello"}]
