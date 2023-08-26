
from ddd.entities.Report import Report

class ReportRepo:
    def __init__(self):
        self.data = {}

    def create(self, entity: Report):
        self.data[entity.id.value] = entity

    def read(self, id: str):
        return self.data.get(id)

    def update(self, id: str, entity: Report):
        self.data[id] = entity

    def delete(self, id: str):
        del self.data[id]
    