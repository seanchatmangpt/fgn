
from ddd.value_objects.FeedbackValue import FeedbackValue

class Feedback:
    def __init__(self, id: FeedbackValue = None):
        self.id = id if id else FeedbackValue()
    