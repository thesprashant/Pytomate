from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pytomate_graphics_scene import OurQGraphicsScene
from pytomate_graphics_view import OurQGraphicsView
from pytomate_scene import Scene
from pytomate_node import Node
from pytomate_edge import Edge, EDGE_TYPE_BEZIER

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

        self.addNodes()

        self.view = OurQGraphicsView(self.Scene.graphicsScene, self)
        self.layout.addWidget(self.view)

        self.setWindowTitle("Pytomate")

        self.show()

    def addNodes(self):
        node1 = Node(self.Scene, "Note ", inputs=[1,2,3], outputs=[1])
        node2 = Node(self.Scene, "Note", inputs=[1,2,3], outputs=[1])
        node3 = Node(self.Scene, "Note", inputs=[1,2,3], outputs=[1])
        node1.setPos(-350, -250)
        node2.setPos(-75, 0)
        node3.setPos(200, -150)

        edge1 = Edge(self.Scene, node1.outputs[0], node2.inputs[0], edge_type=EDGE_TYPE_BEZIER)
        edge2 = Edge(self.Scene, node2.outputs[0], node3.inputs[0], edge_type=EDGE_TYPE_BEZIER)



    def loadStylesheet(self, filename):
        print('STYLE loading:', filename)
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))
