from dataclasses import dataclass
from datetime import datetime

@dataclass
class Record:
    Type: str
    Content: str
    Date: datetime = None

    def __post_init__(self):
        if self.Date is None:
            self.Date = datetime.now()
