
from ddd.repositories.EmployeeRepo import EmployeeRepo

class EmployeeService:
    def __init__(self, repo: EmployeeRepo):
        self.repo = repo

    def perform_operation(self, entity):
        # Logic for performing an operation
        pass
    