from pytomate_graphics_node import OurGraphicsNode


class Node():
    def __init__(self, scene, title="Undefined Node"):
        self.scene = scene

        self.title = title

        self.graphicsNode = OurGraphicsNode(self, self.title)

        self.scene.addNode(self)
        self.scene.graphicsScene.addItem(self.graphicsNode)


        self.inputs = []
        self.outputs = []
