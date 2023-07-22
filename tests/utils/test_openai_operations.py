import pytest
import os
import tempfile
import shutil

from unittest.mock import MagicMock, patch

from fgn.utils.openai_operations import (
    save_completion,
    gpt3_completion,
    gpt_chat_completion,
    gpt4_completion,
    generate_filename,
    generate_output_file,
)


@pytest.fixture(autouse=True)
def mock_save_to_project_folder(monkeypatch):
    # Mock save_to_project_folder
    mock_save = MagicMock()
    monkeypatch.setattr("fgn.utils.openai_operations.save_to_project_folder", mock_save)
    return mock_save


# Use pytest fixtures for setup and teardown
@pytest.fixture
def openai_operations_fixture():
    with patch("openai.Completion.create") as mock_openai_completion, patch(
        "openai.ChatCompletion.create"
    ) as mock_openai_chat_completion:
        temp_dir = tempfile.mkdtemp()
        yield mock_openai_completion, mock_openai_chat_completion, temp_dir
        shutil.rmtree(temp_dir)


def test_gpt3_completion(openai_operations_fixture):
    mock_openai_completion, _, _ = openai_operations_fixture
    completion_text = "Test GPT-3 completion"
    mock_openai_completion.return_value = {"choices": [{"text": completion_text}]}
    result = gpt3_completion("Test prompt")
    assert result.strip() == completion_text.strip()


def test_chat_completion(openai_operations_fixture):
    _, mock_openai_chat_completion, _ = openai_operations_fixture
    completion_text = "Test chat completion"
    mock_openai_chat_completion.return_value = {
        "choices": [{"message": {"content": completion_text}}]
    }
    result = gpt_chat_completion(
        messages=[{"role": "user", "content": "Test prompt"}], model="gpt-4"
    )
    assert result.strip() == completion_text.strip()


@patch("fgn.utils.openai_operations.gpt_chat_completion")
def test_gpt4_completion(mock_chat_completion):
    completion_text = "Test GPT-4 completion"
    mock_chat_completion.return_value = completion_text
    result = gpt4_completion("Test prompt")
    assert result.strip() == completion_text.strip()


@patch("fgn.utils.openai_operations.gpt3_completion")
def test_generate_filename(mocked_gpt3_completion):
    mocked_gpt3_completion.return_value = "test_filename"
    filename = generate_filename(
        prompt="Test prompt",
        prefix="prefix",
        suffix="suffix",
        extension="py",
        max_chars=60,
        time=False,
    )
    assert filename == "prefix_test_filename_suffix.py"


@patch("fgn.utils.openai_operations.gpt3_completion")
def test_generate_output_file(mocked_gpt3_completion):
    mocked_gpt3_completion.return_value = "test_output_file"
    output_file = generate_output_file(
        prompt="Test prompt", extension="py", max_chars=60, time=False
    )
    assert output_file == "test_output_file.py"


@patch("fgn.utils.openai_operations.openai.Completion.create")
def test_gpt3_completion_with_different_stop_sequences(mock_openai_completion):
    completion_text = "Test GPT-3 completion with stop sequence"
    mock_openai_completion.return_value = {"choices": [{"text": completion_text}]}
    result = gpt3_completion("Test prompt", stop=["<<STOP>>", "<<END>>"])
    assert result.strip() == completion_text.strip()


@patch("fgn.utils.openai_operations.openai.ChatCompletion.create")
def test_gpt_chat_completion_max_context_length_error(mock_openai_chat_completion):
    error_message = "Error: Maximum context length exceeded"
    mock_openai_chat_completion.side_effect = Exception(error_message)
    result = gpt_chat_completion(
        messages=[{"role": "user", "content": "Test prompt"}],
        model="gpt-4",
        max_retry=3,
        backoff_factor=0.0001,
        initial_wait=0.0001,
    )
    assert result == f"GPT error: {error_message}"
