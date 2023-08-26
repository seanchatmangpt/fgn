
from ddd.entities.Email import Email

class EmailAggregate:
    def __init__(self, root_entity: Email):
        self.root_entity = root_entity
    