
from ddd.entities.Feedback import Feedback

class FeedbackAggregate:
    def __init__(self, root_entity: Feedback):
        self.root_entity = root_entity
    