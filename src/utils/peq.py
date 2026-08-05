from __future__ import annotations

import ast
import hashlib
import importlib.util
import inspect
import shlex
import sys
import textwrap
from pathlib import Path
from types import ModuleType
from typing import Any

from fgn.core.broker import Broker, Receipt


class Peq:
    """Receipt-bound Python module editor with deterministic undo and redo."""

    _INTERNAL = {
        "filepath",
        "module",
        "history",
        "current_state",
        "templates",
        "broker",
        "receipts",
    }

    def __init__(self, filepath, source=None, *, broker: Broker | None = None):
        object.__setattr__(self, "filepath", str(filepath))
        object.__setattr__(self, "module", None)
        object.__setattr__(self, "history", [])
        object.__setattr__(self, "current_state", -1)
        object.__setattr__(self, "templates", {})
        object.__setattr__(self, "broker", broker or Broker())
        object.__setattr__(self, "receipts", [])
        self._ensure_module_exists(source)
        self._load_module()
        self._capture_state()

    @property
    def path(self) -> Path:
        return Path(self.filepath)

    def _write(self, content: str) -> Receipt:
        receipt = self.broker.write_text(self.path, content)
        self.receipts.append(receipt)
        return receipt

    def _ensure_module_exists(self, source):
        if not self.path.exists():
            self._write(source if source is not None else "# Auto-generated module\n")

    def _module_name(self) -> str:
        digest = hashlib.sha256(str(self.path.resolve()).encode()).hexdigest()[:12]
        return f"peq_{self.path.stem}_{digest}"

    def _load_module(self):
        module_name = self._module_name()
        sys.modules.pop(module_name, None)
        spec = importlib.util.spec_from_file_location(module_name, self.path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Unable to load module from {self.path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[module_name] = module
        object.__setattr__(self, "module", module)

    def _capture_state(self):
        content = self.path.read_text(encoding="utf-8")
        history = self.history[: self.current_state + 1]
        if not history or history[-1] != content:
            history.append(content)
        object.__setattr__(self, "history", history)
        object.__setattr__(self, "current_state", len(history) - 1)

    def __getattr__(self, key):
        module = object.__getattribute__(self, "module")
        return getattr(module, key)

    def __setattr__(self, key, new_item):
        if key in self._INTERNAL:
            object.__setattr__(self, key, new_item)
            return
        self._modify_module(key, new_item)

    @staticmethod
    def _callable_node(key: str, value: Any) -> ast.AST:
        source = textwrap.dedent(inspect.getsource(value))
        node = ast.parse(source).body[0]
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            node.name = key
        return node

    @staticmethod
    def _node_for(key: str, new_item: Any) -> ast.AST:
        if isinstance(new_item, ast.AST):
            return new_item
        if callable(new_item):
            return Peq._callable_node(key, new_item)
        if isinstance(new_item, str):
            parsed = ast.parse(new_item).body
            if len(parsed) != 1:
                raise ValueError("A string edit must contain exactly one top-level statement")
            return parsed[0]
        return ast.Assign(
            targets=[ast.Name(id=key, ctx=ast.Store())],
            value=ast.parse(repr(new_item), mode="eval").body,
        )

    @staticmethod
    def _node_identity(node: ast.AST) -> tuple[type[ast.AST], str | None]:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            return type(node), node.name
        if isinstance(node, ast.Assign) and node.targets and isinstance(node.targets[0], ast.Name):
            return ast.Assign, node.targets[0].id
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            return type(node), ast.unparse(node)
        return type(node), None

    def _modify_module(self, key, new_item):
        tree = ast.parse(self.path.read_text(encoding="utf-8"))
        node = self._node_for(key, new_item)
        node_type, node_name = self._node_identity(node)
        replacement = None
        for index, existing in enumerate(tree.body):
            existing_type, existing_name = self._node_identity(existing)
            if existing_type is node_type and existing_name == node_name:
                replacement = index
                break
        if replacement is None:
            tree.body.append(node)
        else:
            tree.body[replacement] = node
        ast.fix_missing_locations(tree)
        content = ast.unparse(tree).rstrip() + "\n"
        self._write(content)
        self._load_module()
        self._capture_state()

    def replace_module_content(self, new_content):
        self._write(new_content)
        self._load_module()
        self._capture_state()

    def undo(self) -> bool:
        if self.current_state <= 0:
            return False
        target = self.current_state - 1
        self._write(self.history[target])
        object.__setattr__(self, "current_state", target)
        self._load_module()
        return True

    def redo(self) -> bool:
        if self.current_state >= len(self.history) - 1:
            return False
        target = self.current_state + 1
        self._write(self.history[target])
        object.__setattr__(self, "current_state", target)
        self._load_module()
        return True

    def add_import(self, statement: str) -> None:
        node = ast.parse(statement).body[0]
        if not isinstance(node, (ast.Import, ast.ImportFrom)):
            raise ValueError("statement must be an import")
        self._modify_module(ast.unparse(node), node)

    def test(self, *pytest_args: str):
        command = shlex.join([sys.executable, "-m", "pytest", *pytest_args])
        return self.broker.run_shell(command, admitted=True, cwd=self.path.parent)
