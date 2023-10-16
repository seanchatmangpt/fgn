import ast
import importlib.util
import os
import sys


class Peq:
    def __init__(self, filepath, source=None):
        self.filepath = filepath
        self.module = None  # Placeholder for the module type
        self.history = []
        self.current_state = (
            -1
        )  # We'll increment this whenever a new state is added to history
        self.templates = {}

        self._ensure_module_exists(source)
        self._load_module()
        self._capture_state()

    def _ensure_module_exists(self, source):
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w") as f:
                content = source if source else "# Auto-generated module\n"
                f.write(content)

    def _load_module(self):
        module_name = self.filepath.replace(".py", "")
        if module_name in sys.modules:
            del sys.modules[module_name]
        spec = importlib.util.spec_from_file_location(module_name, self.filepath)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    def _capture_state(self):
        with open(self.filepath, "r") as f:
            current_content = f.read()
        self.history.append(current_content)
        self.current_state += 1

    def __getattr__(self, key):
        return getattr(self.module, key)

    def __setattr__(self, key, new_item):
        # Check if it's one of the internal attributes first
        if key in ["filepath", "module", "history", "current_state", "templates"]:
            self.__dict__[key] = new_item
            return

        # Otherwise, treat it as a module attribute
        self._modify_module(key, new_item)

    def _modify_module(self, key, new_item):
        # Read the existing code
        with open(self.filepath, "r") as f:
            old_code = f.read()
        old_ast = ast.parse(old_code)

        # Convert string to AST if necessary
        if isinstance(new_item, str):
            new_item_ast = ast.parse(new_item).body[0]
        else:
            new_item_ast = new_item

        # Determine whether to replace an existing item or add a new one
        if isinstance(new_item_ast, (ast.FunctionDef, ast.AsyncFunctionDef)):
            existing_indices = [
                i
                for i, node in enumerate(old_ast.body)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                   and node.name == key
            ]
        elif isinstance(new_item_ast, ast.ClassDef):
            existing_indices = [
                i
                for i, node in enumerate(old_ast.body)
                if isinstance(node, ast.ClassDef) and node.name == key
            ]
        elif isinstance(new_item_ast, ast.Assign):
            existing_indices = [
                i
                for i, node in enumerate(old_ast.body)
                if isinstance(node, ast.Assign) and node.targets[0].id == key
            ]
        else:
            raise ValueError("The new item must be a function, class definition, or an assignment.")

        if existing_indices:
            old_ast.body[existing_indices[0]] = new_item_ast
        else:
            old_ast.body.append(new_item_ast)

        # Compile and execute the modified AST to update the module
        new_code = compile(old_ast, filename=self.filepath, mode="exec")
        exec(new_code, self.module.__dict__)

        # Write back the modified code to the file
        with open(self.filepath, "w") as f:
            f.write(ast.unparse(old_ast))
        self._capture_state()  # Capture the modified state

    def replace_module_content(self, new_content):
        with open(self.filepath, "w") as f:
            f.write(new_content)
        self._load_module()
        self._capture_state()  # Capture the new module state

