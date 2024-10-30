from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene


class OurQGraphicsView(QGraphicsView):
    def __init__(self, graphicsScene, parent=None):
        super().__init__(parent)
        self.graphicsScene = graphicsScene

        self.initui()

        self.setScene(self.graphicsScene)
    def initui(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
