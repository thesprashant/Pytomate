from PyQt5.QtWidgets import *


class OurNodeContentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        self.wdg_label = QLineEdit()
        self.wdg_label.setPlaceholderText("Title")
        self.layout.addWidget(self.wdg_label)
        self.text=QTextEdit()
        self.text.setPlaceholderText("Enter Note: ")
        self.layout.addWidget(self.text)
