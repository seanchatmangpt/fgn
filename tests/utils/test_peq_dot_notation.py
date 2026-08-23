from fgn.core.broker import Broker
from utils.peq import Peq


def test_add_function_using_dot_notation(tmp_path):
    target = tmp_path / "sample_module.py"
    peq = Peq(target, broker=Broker(receipt_dir=tmp_path / "receipts"))

    def greet():
        return "Hello, World!"

    peq.greet = greet
    assert peq.module.greet() == "Hello, World!"
