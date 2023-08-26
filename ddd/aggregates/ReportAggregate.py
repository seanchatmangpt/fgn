
from ddd.entities.Report import Report

class ReportAggregate:
    def __init__(self, root_entity: Report):
        self.root_entity = root_entity
    