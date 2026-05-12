from PySide6.QtWidgets import QWidget, QPlainTextEdit, QVBoxLayout, QGroupBox


class Console(QWidget):
    def __init__(self):
        super().__init__()
        pageLayout = QVBoxLayout()
        groupBox = QGroupBox("Console")
        groupLayout = QVBoxLayout()

        self.Textbox = QPlainTextEdit(readOnly=True)

        pageLayout.addWidget(groupBox)
        groupBox.setLayout(groupLayout)
        groupLayout.addWidget(self.Textbox)

        self.setLayout(pageLayout)

    def clear(self):
        self.Textbox.clear()

    def setText(self, text):
        self.Textbox.setPlainText(text)

    def appendText(self, text):
        self.Textbox.appendPlainText(text)