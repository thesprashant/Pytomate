from collections import OrderedDict
from pytomate_serializable import Serializable

from PyQt5.QtWidgets import *


class OurNodeContentWidget(QWidget, Serializable):
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

    def serialize(self):
        return OrderedDict([

        ])

    def deserialize(self, data, hashmap={}):
        return False

