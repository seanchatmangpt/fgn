
from ddd.repositories.ReportRepo import ReportRepo

class ReportService:
    def __init__(self, repo: ReportRepo):
        self.repo = repo

    def perform_operation(self, entity):
        # Logic for performing an operation
        pass
    