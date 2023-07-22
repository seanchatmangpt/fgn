import pytest
from unittest.mock import MagicMock
from fgn.utils.output_manager import OutputManager


# Set up your mocks at the top of the file
@pytest.fixture(autouse=True)
def mock_open(mocker):
    mocker.patch("builtins.open", mocker.mock_open())
    return open


@pytest.fixture(autouse=True)
def mock_pyperclip_copy(mocker):
    mock_copy = mocker.patch("pyperclip.copy")
    return mock_copy


@pytest.fixture
def output_manager():
    return OutputManager()


def test_handle_output_no_flags(mock_open, mock_pyperclip_copy, output_manager):
    response = "Test response"
    output_manager.handle_output(response)

    mock_pyperclip_copy.assert_called_once_with(response)
    mock_open.assert_not_called()  # since neither 'output' nor 'auto_output' flags are set


def test_handle_output_output_flag(mock_open, mock_pyperclip_copy, output_manager):
    response = "Test response"
    output_manager.output = "test_output.md"
    output_manager.handle_output(response)

    mock_pyperclip_copy.assert_called_once_with(response)
    mock_open.assert_called_once()  # since 'output' flag is set


def test_handle_output_auto_output_flag(mock_open, mock_pyperclip_copy, output_manager):
    response = "Test response"
    output_manager.auto_output = True
    output_manager.handle_output(response)

    mock_pyperclip_copy.assert_called_once_with(response)
    mock_open.assert_called()  # since 'auto_output' flag is set


def test_handle_output_no_copy_flag(mock_open, mock_pyperclip_copy, output_manager):
    response = "Test response"
    output_manager.no_copy = True
    output_manager.handle_output(response)

    mock_pyperclip_copy.assert_not_called()  # since 'no_copy' flag is set
    mock_open.assert_not_called()  # since neither 'output' nor 'auto_output' flags are set


def test_save_to_file_no_filename(mock_open, output_manager):
    response = "Test response"
    output_manager.save_to_file(response)

    mock_open.assert_called()
    handle = mock_open()
    handle.write.assert_called_with(response)


def test_save_to_file_with_filename(mock_open, output_manager):
    response = "Test response"
    filename = "test_output.md"
    output_manager.save_to_file(response, filename)

    mock_open.assert_called_once_with(filename, 'w')
    file_handle = mock_open.return_value.__enter__.return_value
    file_handle.write.assert_called_with(response)


def test_save_to_file_append(mock_open, output_manager):
    response = "Test response"
    filename = "test_output.md"
    output_manager.save_to_file(response, filename, append=True)

    mock_open.assert_called_once_with(filename, 'a')
    file_handle = mock_open.return_value.__enter__.return_value
    file_handle.write.assert_called_with('\n\n' + response)
