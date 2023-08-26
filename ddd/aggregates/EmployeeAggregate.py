
from ddd.entities.Employee import Employee

class EmployeeAggregate:
    def __init__(self, root_entity: Employee):
        self.root_entity = root_entity
    