from collections import OrderedDict
from pytomate_serializable import Serializable
from pytomate_content_widget import OurNodeContentWidget
from pytomate_graphics_node import OurGraphicsNode
from pytomate_socket import *
from pytomate_utils import dumpException


DEBUG = False
class Node(Serializable):
    def __init__(self, scene, title="Undefined Node", inputs=[], outputs=[]):
        super().__init__()
        self._title = title
        self.scene = scene

        self.initInnerClasses()
        self.initSettings()

        self.title = title

        self.scene.addNode(self)
        self.scene.graphicsScene.addItem(self.grNode)


        # create socket for inputs and outputs
        self.inputs = []
        self.outputs = []
        self.initSockets(inputs, outputs)

        self._is_dirty = False
        self._is_invalid = False


    def initInnerClasses(self):
        self.content = OurNodeContentWidget(self)
        self.grNode = OurGraphicsNode(self)

    def initSettings(self):
        self.socket_spacing = 22

        self.input_socket_position = LEFT_BOTTOM
        self.output_socket_position = RIGHT_TOP
        self.input_multi_edged = False
        self.output_multi_edged = True

    def initSockets(self, inputs, outputs, reset=True):
        """ Create sockets for inputs and outputs"""

        if reset:
            # clear old sockets
            if hasattr(self, 'inputs') and hasattr(self, 'outputs'):
                # remove grSockets from scene
                for socket in (self.inputs + self.outputs):
                    self.scene.graphicsScene.removeItem(socket.grSocket)
                self.inputs = []
                self.outputs = []

        counter = 0
        for item in inputs:
            socket = Socket(node=self, index=counter, position=self.input_socket_position,
                            socket_type=item, multi_edges=self.input_multi_edged, is_input=True)
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            socket = Socket(node=self, index=counter, position=self.output_socket_position,
                            socket_type=item, multi_edges=self.output_multi_edged, is_input=False)
            counter += 1
            self.outputs.append(socket)

    def onEdgeConnectionChanged(self, new_edge):
        print("%s::onEdgeConnectionChanged" % self.__class__.__name__, new_edge)

    def onInputChanged(self, new_edge):
        print("%s::onInputChanged" % self.__class__.__name__, new_edge)
        self.markDirty()
        self.markDescendantsDirty()



    def __str__(self):
        return "<Node %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])



    @property
    def pos(self):
        return self.grNode.pos()  # QPointF

    def setPos(self, x, y):
        self.grNode.setPos(x, y)

    @property
    def title(self): return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.grNode.title = self._title


    def getSocketPosition(self, index, position):
        x = 0 if (position in (LEFT_TOP, LEFT_BOTTOM)) else self.grNode.width

        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            # start from bottom
            y = self.grNode.height - self.grNode.edge_size - self.grNode._padding - index * self.socket_spacing
        else:
            # start from top
            y = self.grNode.title_height + self.grNode._padding + self.grNode.edge_size + index * self.socket_spacing

        return x, y
        return [x, y]


    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            for edge in socket.edges:
                edge.updatePositions()

    def remove(self):
        if DEBUG: print("> Removing Node", self)
        if DEBUG: print(" - remove all edges from sockets")
        for socket in (self.inputs+self.outputs):
            for edge in socket.edges:
                if DEBUG: print("    - removing from socket:", socket, "edges:", edge)
                edge.remove()
        if DEBUG: print(" - remove grNode")
        self.scene.graphicsScene.removeItem(self.grNode)
        self.grNode = None
        if DEBUG: print(" - remove node from the scene")
        self.scene.removeNode(self)
        if DEBUG: print(" - everything was done.")

    def isDirty(self):
        return self._is_dirty

    def markDirty(self, new_value=True):
        self._is_dirty = new_value
        if self._is_dirty: self.onMarkedDirty()

    def onMarkedDirty(self): pass

    def markChildrenDirty(self, new_value=True):
        for other_node in self.getChildrenNodes():
            other_node.markDirty(new_value)

    def markDescendantsDirty(self, new_value=True):
        for other_node in self.getChildrenNodes():
            other_node.markDirty(new_value)
            other_node.markChildrenDirty(new_value)

    def isInvalid(self):
        return self._is_invalid

    def markInvalid(self, new_value=True):
        self._is_invalid = new_value
        if self._is_invalid: self.onMarkedInvalid()

    def onMarkedInvalid(self): pass

    def markChildrenInvalid(self, new_value=True):
        for other_node in self.getChildrenNodes():
            other_node.markInvalid(new_value)

    def markDescendantsInvalid(self, new_value=True):
        for other_node in self.getChildrenNodes():
            other_node.markInvalid(new_value)
            other_node.markChildrenInvalid(new_value)

    def eval(self):
        self.markDirty(False)
        self.markInvalid(False)
        return 0

    def evalChildren(self):
        for node in self.getChildrenNodes():
            node.eval()

    # traversing nodes functions

    def getChildrenNodes(self):
        if self.outputs == []: return []
        other_nodes = []
        for ix in range(len(self.outputs)):
            for edge in self.outputs[ix].edges:
                other_node = edge.getOtherSocket(self.outputs[ix]).node
                other_nodes.append(other_node)
        return other_nodes

    def getInput(self, index=0):
        try:
            edge = self.inputs[index].edges[0]
            socket = edge.getOtherSocket(self.inputs[index])
            return socket.node
        except IndexError:
            print("Trying to get input but none attached", self)
            return None
        except Exception as e:
            dumpException(e)
            return None

    def getInputs(self, index=0):
        ins = []
        for edge in self.inputs[index].edges:
            other_socket = edge.getOtherSocket(self.inputs[index])
            ins.append(other_socket.node)
        return ins

    def getOutputs(self, index=0):
        outs = []
        for edge in self.outputs[index].edges:
            other_socket = edge.getOtherSocket(self.outputs[index])
            outs.append(other_socket.node)
        return outs



    def serialize(self):
        inputs, outputs = [], []
        for socket in self.inputs: inputs.append(socket.serialize())
        for socket in self.outputs: outputs.append(socket.serialize())
        return OrderedDict([
            ('id', self.id),
            ('title', self.title),
            ('pos_x', self.grNode.scenePos().x()),
            ('pos_y', self.grNode.scenePos().y()),
            ('inputs', inputs),
            ('outputs', outputs),
            ('content', self.content.serialize()),
        ])

    def deserialize(self, data, hashmap={}, restore_id=True):
        try:
            if restore_id: self.id = data['id']
            hashmap[data['id']] = self

            self.setPos(data['pos_x'], data['pos_y'])
            self.title = data['title']

            data['inputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000 )
            data['outputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000 )

            self.inputs = []
            for socket_data in data['inputs']:
                new_socket = Socket(node=self, index=socket_data['index'], position=socket_data['position'],
                                    socket_type=socket_data['socket_type'])
                new_socket.deserialize(socket_data, hashmap, restore_id)
                self.inputs.append(new_socket)

            self.outputs = []
            for socket_data in data['outputs']:
                new_socket = Socket(node=self, index=socket_data['index'], position=socket_data['position'],
                                    socket_type=socket_data['socket_type'])
                new_socket.deserialize(socket_data, hashmap, restore_id)
                self.outputs.append(new_socket)
        except Exception as e: dumpException(e)

        res = self.content.deserialize(data['content'], hashmap)

        return True & res
