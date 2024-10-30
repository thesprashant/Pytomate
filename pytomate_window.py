from PyQt5.QtWidgets import QWidget, QGraphicsView, QVBoxLayout, QGraphicsScene
from pytomate_graphics_scene import OurQGraphicsScene
from pytomate_graphics_view import OurQGraphicsView
from pytomate_scene import Scene
from pytomate_node import Node

class PytomateWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initialise_ui()


    def initialise_ui(self):
        self.setGeometry(300, 150, 1280, 720)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.Scene = Scene()

        node = Node(self.Scene, "Note")

        self.view = OurQGraphicsView(self.Scene.graphicsScene, self)
        self.layout.addWidget(self.view)

        self.setWindowTitle("Pytomate")

        self.show()