
from ddd.entities.Email import Email

class EmailRepo:
    def __init__(self):
        self.data = {}

    def create(self, entity: Email):
        self.data[entity.id.value] = entity

    def read(self, id: str):
        return self.data.get(id)

    def update(self, id: str, entity: Email):
        self.data[id] = entity

    def delete(self, id: str):
        del self.data[id]
    