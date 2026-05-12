from dataclasses import dataclass
from .Record import Record

@dataclass
class Card:
    UID: str
    Records: dict[int, list[Record]]

    def addRecord(self, id: int, record: Record):
        if id not in self.Records:
            self.Records[id] = []
        self.Records[id].append(record)

    def asList(self):
        return list(self.Records.values())

    def getRecord(self, id: int):
        return self.Records[id]


