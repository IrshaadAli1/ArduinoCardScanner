from dataclasses import dataclass
import serial_asyncio
import sys
from PySide6.QtWidgets import QApplication, QTreeWidgetItem, QWidget
from PySide6 import QtAsyncio

from gui import GUI
from card import Card, Record
from datetime import datetime


@dataclass
class TreeItemContainer:
    Widget: QTreeWidgetItem
    Children: dict[int, TreeItemContainer]


class Run:
    def __init__(self):
        self.Active = False
        self.Cards = {}
        self.CardTreeItems = {}

        self.Writer = self.Reader = None

        self.app = QApplication(sys.argv)
        self.UI = GUI()

    def run(self):
        self.UI.show()
        QtAsyncio.run(self.runSerial())


    async def handleCard(self, uid):
        if uid not in self.Cards:
            self.Cards[uid] = Card(uid, {})
            self.CardTreeItems[uid] = TreeItemContainer(QTreeWidgetItem(self.UI.LogTree.Tree, [uid]), {})

        return self.Cards[uid]


    async def handleData(self, data: dict):
        UID = data["UID"]
        card = await self.handleCard(UID)
        dateTime = datetime.now()
        for recordID, record in data["Records"].items():
            record = Record(record["Type"], record["Content"], dateTime)
            card.addRecord(recordID, record)

            cardTree = self.CardTreeItems[UID]
            if record.Date not in cardTree.Children:
                dateTree = TreeItemContainer(QTreeWidgetItem(cardTree.Widget, [str(record.Date) + (f" ({record.Date - list(cardTree.Children.keys())[-1]})" if len(cardTree.Children) > 0 else "")]), {})
                cardTree.Children[record.Date] = dateTree
            dateTree = cardTree.Children[record.Date]
            dateTree.Children[recordID] = QTreeWidgetItem(dateTree.Widget, [recordID, record.Type, record.Content])

    async def runSerial(self):
        self.Active = True

        try:
            self.Reader, self.Writer = await serial_asyncio.open_serial_connection(url="COM5", baudrate=9600)
            while self.Active:
                data = await self.Reader.readline()
                if data == "": continue
                line = data.decode("utf-8").strip()
                try:
                    evalData = eval(line)
                    print(evalData)
                    await self.handleData(evalData)
                except Exception as e:
                    print(e)
                print(line)

            self.Writer.close()
            await self.Writer.wait_closed()
        except Exception as e:
            self.Active = False

if __name__ == "__main__":
    Run().run()
