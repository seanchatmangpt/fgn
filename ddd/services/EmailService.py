
from ddd.repositories.EmailRepo import EmailRepo

class EmailService:
    def __init__(self, repo: EmailRepo):
        self.repo = repo

    def perform_operation(self, entity):
        # Logic for performing an operation
        pass
    