from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from fgn.utils.llm_operations import (
    LLMProviderError,
    generate_filename,
    generate_output_file,
    gpt3_completion,
    gpt4_completion,
    gpt_chat_completion,
)


class FakeCompletions:
    def __init__(self, *, content=None, error=None):
        self.content = content
        self.error = error
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if self.error is not None:
            raise self.error
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=self.content))]
        )


class FakeClient:
    def __init__(self, *, content=None, error=None):
        self.completions = FakeCompletions(content=content, error=error)
        self.chat = SimpleNamespace(completions=self.completions)


@pytest.fixture(autouse=True)
def mock_save_to_project_folder(monkeypatch):
    mock_save = MagicMock()
    monkeypatch.setattr("fgn.utils.llm_operations.save_to_project_folder", mock_save)
    return mock_save


def test_gpt3_completion_uses_modern_chat_client():
    client = FakeClient(content="Test GPT-3 completion")
    result = gpt3_completion("Test prompt", client=client)
    assert result == "Test GPT-3 completion"
    assert client.completions.calls[0]["messages"] == [
        {"role": "user", "content": "Test prompt"}
    ]


def test_chat_completion_uses_injected_client():
    client = FakeClient(content="Test chat completion")
    result = gpt_chat_completion(
        messages=[{"role": "user", "content": "Test prompt"}],
        model="gpt-4o-mini",
        client=client,
    )
    assert result == "Test chat completion"


@patch("fgn.utils.llm_operations.gpt_chat_completion")
def test_gpt4_completion(mock_chat_completion):
    mock_chat_completion.return_value = "Test GPT-4 completion"
    result = gpt4_completion("Test prompt")
    assert result == "Test GPT-4 completion"


def test_generate_filename_is_deterministic():
    filename = generate_filename(
        prompt="Test prompt",
        prefix="prefix",
        suffix="suffix",
        extension="py",
        max_chars=60,
        time=False,
    )
    assert filename == "prefix_test_prompt_suffix.py"


def test_generate_output_file_is_deterministic():
    output_file = generate_output_file(
        prompt="Test output file", extension="py", max_chars=60, time=False
    )
    assert output_file == "test_output_file.py"


def test_gpt3_completion_accepts_legacy_stop_argument():
    client = FakeClient(content="Stopped completion")
    result = gpt3_completion(
        "Test prompt",
        stop=["<<STOP>>", "<<END>>"],
        client=client,
    )
    assert result == "Stopped completion"


def test_context_length_error_is_typed():
    client = FakeClient(error=RuntimeError("Maximum context length exceeded"))
    with pytest.raises(LLMProviderError) as exc_info:
        gpt_chat_completion(
            messages=[{"role": "user", "content": "Test prompt"}],
            model="gpt-4o-mini",
            max_retry=3,
            backoff_factor=0.0001,
            initial_wait=0.0001,
            client=client,
            sleep_fn=lambda _: None,
        )
    assert exc_info.value.code == "CONTEXT_LENGTH_EXCEEDED"
