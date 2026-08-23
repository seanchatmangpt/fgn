import os
from pathlib import Path

from fgn.core.broker import Broker, Receipt


def create_init_files(directory: str = ".", verbose: bool = False) -> list[Receipt]:
    """Create missing package markers through BRCE and return their receipts."""
    roots = [Path(root) for root, _, _ in os.walk(directory)]
    broker = Broker()
    receipts: list[Receipt] = []
    receipt_root = broker.receipt_dir.resolve()
    for root in roots:
        if root.resolve() == receipt_root or root.resolve().is_relative_to(receipt_root):
            continue
        init_file = root / "__init__.py"
        if init_file.exists():
            continue
        receipt = broker.write_text(init_file, "")
        receipts.append(receipt)
        if verbose:
            print(f"Created {init_file}; receipt={receipt.receipt_id}")
    return receipts
