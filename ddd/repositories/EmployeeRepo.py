
from ddd.entities.Employee import Employee

class EmployeeRepo:
    def __init__(self):
        self.data = {}

    def create(self, entity: Employee):
        self.data[entity.id.value] = entity

    def read(self, id: str):
        return self.data.get(id)

    def update(self, id: str, entity: Employee):
        self.data[id] = entity

    def delete(self, id: str):
        del self.data[id]
    