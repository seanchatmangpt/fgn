
from ddd.value_objects.EmailValue import EmailValue

class Email:
    def __init__(self, id: EmailValue = None):
        self.id = id if id else EmailValue()
    