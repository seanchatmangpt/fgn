"""
    Dummy conftest.py for fgn.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

import pytest
import sys
# Remove user directory if present to avoid importing from /Users/sac instead of /Users/sac/fgn/src
sys.path = [p for p in sys.path if p != "/Users/sac"]
print("CONFTEST PATH:", sys.path)
import fgn
print("FGN PATH IN CONFTEST:", fgn.__path__)


@pytest.fixture(scope="function")


def peq():
    return [None]

