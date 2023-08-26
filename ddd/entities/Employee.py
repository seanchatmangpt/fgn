
from ddd.value_objects.EmployeeValue import EmployeeValue

class Employee:
    def __init__(self, id: EmployeeValue = None):
        self.id = id if id else EmployeeValue()
    