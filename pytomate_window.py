from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pytomate_graphics_scene import OurQGraphicsScene
from pytomate_graphics_view import OurQGraphicsView
from pytomate_scene import Scene
from pytomate_node import Node
from pytomate_socket import Socket

class PytomateWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stylesheet_filename = 'qss/nodestyle.qss'
        self.loadStylesheet(self.stylesheet_filename)


        self.initialise_ui()


    def initialise_ui(self):
        self.setGeometry(300, 150, 1280, 720)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.Scene = Scene()

        node = Node(self.Scene, "Note", inputs=[1,2,3], outputs=[1])

        self.view = OurQGraphicsView(self.Scene.graphicsScene, self)
        self.layout.addWidget(self.view)

        self.setWindowTitle("Pytomate")

        self.show()

    def loadStylesheet(self, filename):
        print('STYLE loading:', filename)
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))
