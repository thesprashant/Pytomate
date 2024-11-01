import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pytomate_graphics_scene import OurQGraphicsScene
from pytomate_graphics_view import OurQGraphicsView
from pytomate_scene import Scene, InvalidFile
from pytomate_node import Node
from pytomate_edge import Edge, EDGE_TYPE_BEZIER

from pytomate_socket import Socket

class PytomateWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stylesheet_filename = 'qss/nodestyle.qss'
        self.loadStylesheet(self.stylesheet_filename)

        self.filename = None

        self.initialise_ui()


    def initialise_ui(self):

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.Scene = Scene()


        self.view = OurQGraphicsView(self.Scene.graphicsScene, self)
        self.layout.addWidget(self.view)

        self.setWindowTitle("Pytomate")

        self.show()

    def isModified(self):
        return self.Scene.isModified()


    def isFilenameSet(self):
        return self.filename is not None

    def getSelectedItems(self):
        return self.Scene.getSelectedItems()

    def hasSelectedItems(self):
        return self.getSelectedItems() != []

    def canUndo(self):
        return self.Scene.history.canUndo()

    def canRedo(self):
        return self.Scene.history.canRedo()


    def getUserFriendlyFilename(self):
        name = os.path.basename(self.filename) if self.isFilenameSet() else "New Automation Graph"
        return name + ("*" if self.isModified() else "")

    def fileNew(self):
        self.Scene.clear()
        self.filename = None
        self.Scene.history.clear()
        self.Scene.history.storeInitialHistoryStamp()

    def fileLoad(self, filename):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            self.Scene.loadFromFile(filename)
            self.filename = filename
            self.Scene.history.clear()
            self.Scene.history.storeInitialHistoryStamp()

            return True
        except InvalidFile as e:
            print(e)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, "Error loading %s" % os.path.basename(filename), str(e))
            return False
        finally:
            QApplication.restoreOverrideCursor()


    def fileSave(self, filename=None):
        # when called with empty parameter, we won't store the filename
        if filename is not None: self.filename = filename
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.Scene.saveToFile(self.filename)
        QApplication.restoreOverrideCursor()
        return True


    def addNodes(self):
        node1 = Node(self.Scene, "Note ", inputs=[1,2,3], outputs=[1])
        node2 = Node(self.Scene, "Note", inputs=[1,2,3], outputs=[1])
        node3 = Node(self.Scene, "Note", inputs=[1,2,3], outputs=[1])
        node1.setPos(-350, -250)
        node2.setPos(-75, 0)
        node3.setPos(200, -150)

        edge1 = Edge(self.Scene, node1.outputs[0], node2.inputs[0], edge_type=EDGE_TYPE_BEZIER)
        edge2 = Edge(self.Scene, node2.outputs[0], node3.inputs[0], edge_type=EDGE_TYPE_BEZIER)

        self.Scene.history.storeInitialHistoryStamp()


    def loadStylesheet(self, filename):
        print('STYLE loading:', filename)
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))
