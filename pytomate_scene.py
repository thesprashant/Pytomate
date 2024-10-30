from pytomate_graphics_scene import OurQGraphicsScene


class Scene:
    def __init__ (self):
        self.nodes = []
        self.edges = []
        self.scene_width = 70000
        self.scene_height = 70000
        self.initui()

    def initui(self):
        self.graphicsScene = OurQGraphicsScene(self)
        self.graphicsScene.setgraphicsScene(self.scene_width, self.scene_height)
    def addNode(self, node):
        self.nodes.append(node)

    def addEdge(self, edge):
        self.edges.append(edge)

    def removeNode(self, node):
        self.nodes.remove(node)

    def removeEdge(self, edge):
        self.edges.remove(edge)