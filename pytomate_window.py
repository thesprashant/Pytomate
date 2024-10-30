from PyQt5.QtWidgets import QWidget, QGraphicsView, QVBoxLayout, QGraphicsScene
from pytomate_graphics_scene import OurQGraphicsScene

class PytomateWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initialise_ui()
    def initialise_ui(self):
        self.setGeometry(300, 150, 1280, 720)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.setWindowTitle("Pytomate")

        #Creating a graphics scene
        self.graphicsScene = OurQGraphicsScene()


        # Creating a graphics view where charts will be shown
        self.view = QGraphicsView(self)
        self.view.setScene(self.graphicsScene)
        self.layout.addWidget(self.view)
        self.show()