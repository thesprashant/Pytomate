from node_content_widget import OurNodeContentWidget
from pytomate_graphics_node import OurGraphicsNode


class Node():
    def __init__(self, scene, title="Undefined Node"):
        self.scene = scene

        self.title = title
        self.content = OurNodeContentWidget()
        self.grNode = OurGraphicsNode(self)

        self.scene.addNode(self)
        self.scene.graphicsScene.addItem(self.grNode)


        self.inputs = []
        self.outputs = []
