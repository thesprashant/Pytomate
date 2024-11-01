from PyQt5.QtCore import *
from pytomate_widget import PytomateWidget


class PytomateSubWindow(PytomateWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setTitle()

        self.Scene.addHasBeenModifiedListener(self.setTitle)


    def setTitle(self):
        self.setWindowTitle(self.getUserFriendlyFilename())
