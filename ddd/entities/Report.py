
from ddd.value_objects.ReportValue import ReportValue

class Report:
    def __init__(self, id: ReportValue = None):
        self.id = id if id else ReportValue()
    