from pathlib import Path

import pytest

from fgn.utils.file_operations import (
    extract_markdown,
    get_norm_path,
    get_project_root,
    open_file,
    open_file_or_raise,
    save_relative_to_base,
)


def test_open_file(tmp_path):
    target = tmp_path / "test.txt"
    target.write_text("test content")
    assert open_file(str(target)) == "test content"


def test_save_relative_to_base(tmp_path, monkeypatch):
    receipt_dir = tmp_path / ".fgn" / "receipts"
    monkeypatch.setenv("FGN_RECEIPT_DIR", str(receipt_dir))
    receipt = save_relative_to_base("test.txt", "test content", tmp_path)
    assert (tmp_path / "test.txt").read_text() == "test content"
    assert receipt.status == "ALIVE"


def test_open_file_or_raise(tmp_path):
    with pytest.raises(FileNotFoundError):
        open_file_or_raise(str(tmp_path / "nonexistent.txt"))
    target = tmp_path / "test.txt"
    target.write_text("test content")
    assert open_file_or_raise(str(target)) == "test content"


def test_extract_markdown():
    assert extract_markdown("```test\nprint('Hello World!')```") == "print('Hello World!')"
    assert extract_markdown("no markdown here") == "no markdown here"


def test_get_project_root():
    assert str(get_project_root()).endswith("fgn")


def test_get_norm_path_windows(monkeypatch):
    monkeypatch.setattr("os.name", "nt")
    assert get_norm_path("/path/to/file") == "\\path\\to\\file"


def test_get_norm_path_non_windows(monkeypatch):
    monkeypatch.setattr("os.name", "posix")
    assert get_norm_path("/path/to/file") == "/path/to/file"
