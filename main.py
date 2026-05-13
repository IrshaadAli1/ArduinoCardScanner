from dataclasses import dataclass
import sys
from datetime import datetime

from PySide6.QtWidgets import QApplication, QTreeWidgetItem
from PySide6.QtCore import QObject, Slot, QIODeviceBase
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo

from gui import GUI
from card import Card, Record


@dataclass
class TreeItemContainer:
    Widget: QTreeWidgetItem
    Children: dict


class Run(QObject):
    def __init__(self):
        super().__init__()

        self.Active = False
        self.Cards = {}
        self.CardTreeItems = {}

        self.serial: QSerialPort = None
        self.buffer = b""

        self.app = QApplication(sys.argv)
        self.UI = GUI()

    def run(self):
        self.UI.show()
        self.setupSerial()
        sys.exit(self.app.exec())

    def setupSerial(self):

        for port in QSerialPortInfo.availablePorts():

            print(port.portName(), port.description())

            if "Arduino" in port.description():
                self.serial = QSerialPort()
                self.serial.setPort(port)

                break

        if self.serial is None:
            print("Serial Port not found")
            return

        self.serial.setBaudRate(QSerialPort.BaudRate.Baud9600)
        self.serial.readyRead.connect(self.readSerial)

        if not self.serial.open(QIODeviceBase.OpenModeFlag.ReadOnly):
            print("Failed to open serial port - Maybe another program is currently running the port?")
            return

        self.Active = True

        print("Serial connected")

    def handleCard(self, uid):
        if uid not in self.Cards:
            self.Cards[uid] = Card(uid, {})
            self.CardTreeItems[uid] = TreeItemContainer(
                QTreeWidgetItem(self.UI.LogTree.Tree, [uid]),
                {}
            )

        return self.Cards[uid]

    def handleData(self, data: dict):
        UID = data["UID"]

        card = self.handleCard(UID)

        dateTime = datetime.now()

        for recordID, record in data["Records"].items():

            record = Record(
                record["Type"],
                record["Content"],
                dateTime
            )

            card.addRecord(recordID, record)

            cardTree = self.CardTreeItems[UID]

            if record.Date not in cardTree.Children:

                deltaText = ""

                if len(cardTree.Children) > 0:
                    previous = list(cardTree.Children.keys())[-1]
                    deltaText = f" ({record.Date - previous})"

                dateTree = TreeItemContainer(
                    QTreeWidgetItem(
                        cardTree.Widget,
                        [str(record.Date) + deltaText]
                    ),
                    {}
                )

                cardTree.Children[record.Date] = dateTree

            dateTree = cardTree.Children[record.Date]

            dateTree.Children[recordID] = QTreeWidgetItem(
                dateTree.Widget,
                [recordID, record.Type, record.Content]
            )

    @Slot()
    def readSerial(self):

        while self.serial.canReadLine():

            line = self.serial.readLine().data()
            print(line)
            try:
                decoded = line.decode("utf-8").strip()

                if not decoded:
                    print(decoded, "is not decoded - Continuing")
                    continue

                evalData = eval(decoded)

                self.handleData(evalData)

            except Exception as e:
                print(e)

if __name__ == "__main__":
    Run().run()