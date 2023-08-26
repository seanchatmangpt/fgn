
from uuid import uuid4

class UUID:
    def __init__(self, value: str = None):
        self.value = str(uuid4()) if value is None else value
    