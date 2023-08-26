
from ddd.repositories.FeedbackRepo import FeedbackRepo

class FeedbackService:
    def __init__(self, repo: FeedbackRepo):
        self.repo = repo

    def perform_operation(self, entity):
        # Logic for performing an operation
        pass
    