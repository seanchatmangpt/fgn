
from ddd.entities.Feedback import Feedback

class FeedbackRepo:
    def __init__(self):
        self.data = {}

    def create(self, entity: Feedback):
        self.data[entity.id.value] = entity

    def read(self, id: str):
        return self.data.get(id)

    def update(self, id: str, entity: Feedback):
        self.data[id] = entity

    def delete(self, id: str):
        del self.data[id]
    