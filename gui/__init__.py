from PySide6.QtWidgets import QTabWidget
from .LogTree import LogTree
from .Console import Console


class GUI(QTabWidget):
    def __init__(self):
        super().__init__()

        self.LogTree = LogTree()
        self.Console = Console()

        self.addTab(self.LogTree, "Card Logs")
        self.addTab(self.Console, "Console")