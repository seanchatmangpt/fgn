from fgn.core.broker import Broker
from utils.peq import Peq


def test_initialize_existing_hello_world_module(tmp_path):
    target = tmp_path / "hello_module.py"
    target.write_text('def hello():\n    return "Hello, World!"\n')
    peq = Peq(target, broker=Broker(receipt_dir=tmp_path / "receipts"))
    assert peq.module is not None
    assert peq.hello() == "Hello, World!"
