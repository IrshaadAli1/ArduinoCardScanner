from PySide6.QtWidgets import QWidget, QTreeWidget, QVBoxLayout, QTreeWidgetItem, QHeaderView


class LogTree(QWidget):
    def __init__(self):
        super().__init__()
        PageLayout = QVBoxLayout()
        self.Tree = QTreeWidget()

        PageLayout.addWidget(self.Tree)

        self.setLayout(PageLayout)
        self.Tree.setHeaderLabels(["Record", "Type", "Content"])

        self.TreeLayout = {}

    def addItem(self, id, parent, *strings, currentLayout=None):
        widget = QTreeWidgetItem(parent, strings)
        if currentLayout is None:
            currentLayout = self.TreeLayout
        currentLayout[id] = {
            "Widget": widget,
            "Children": {}
        }
