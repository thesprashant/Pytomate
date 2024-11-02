import os
import json
from collections import OrderedDict
from pytomate_serializable import Serializable
from pytomate_utils import dumpException
from pytomate_graphics_scene import OurQGraphicsScene
from pytomate_node import Node
from pytomate_edge import Edge
from pytomate_scene_history import SceneHistory
from pytomate_scene_clipboard import SceneClipboard



class InvalidFile(Exception): pass



class Scene(Serializable):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []
        self.scene_width = 70000
        self.scene_height = 70000

        self._has_been_modified = False
        self._last_selected_items = []

        self._has_been_modified_listeners = []
        self._item_selected_listeners = []
        self._items_deselected_listeners = []

        self.node_class_selector = None


        self.initui()
        self.history = SceneHistory(self)
        self.clipboard = SceneClipboard(self)

        self.graphicsScene.itemSelected.connect(self.onItemSelected)
        self.graphicsScene.itemDeselected.connect(self.onItemsDeselected)

    def initui(self):
        self.graphicsScene = OurQGraphicsScene(self)
        self.graphicsScene.setgraphicsScene(self.scene_width, self.scene_height)

    def onItemSelected(self):
        current_selected_items = self.getSelectedItems()
        if current_selected_items != self._last_selected_items:
            self._last_selected_items = current_selected_items
            self.history.storeHistory("Selection Changed")
            for callback in self._item_selected_listeners: callback()


    def onItemsDeselected(self):
        self.resetLastSelectedStates()
        if self._last_selected_items != []:
            self._last_selected_items = []
            self.history.storeHistory("Deselected Everything")
            for callback in self._items_deselected_listeners: callback()

    def isModified(self):
        return self.has_been_modified

    def getSelectedItems(self):
        return self.graphicsScene.selectedItems()


    @property
    def has_been_modified(self):
        return self._has_been_modified

    @has_been_modified.setter
    def has_been_modified(self, value):
        if not self._has_been_modified and value:
            self._has_been_modified = value

            # call all registered listeners
            for callback in self._has_been_modified_listeners: callback()


        self._has_been_modified = value


    def addHasBeenModifiedListener(self, callback):
        self._has_been_modified_listeners.append(callback)

    def itemSelectedListener(self, callback):
        self._item_selected_listeners.append(callback)

    def itemDeselectedListener(self, callback):
        self._items_deselected_listeners.append(callback)

    def addDragEnterListener(self, callback):
        self.graphicsScene.views()[0].addDragEnterListener(callback)

    def addDropListener(self, callback):
        self.graphicsScene.views()[0].addDropListener(callback)

    def resetLastSelectedStates(self):
        for node in self.nodes:
            node.grNode._last_selected_state = False
        for edge in self.edges:
            edge.grEdge._last_selected_state = False

    def addNode(self, node):
        self.nodes.append(node)

    def addEdge(self, edge):
        self.edges.append(edge)

    def removeNode(self, node):
        self.nodes.remove(node)

    def removeEdge(self, edge):
        self.edges.remove(edge)

    def clear(self):
        while len(self.nodes) > 0:
            self.nodes[0].remove()
        self.has_been_modified = False


    def saveToFile(self, filename):
        with open(filename, "w") as file:
            file.write( json.dumps( self.serialize(), indent=4 ) )
            print("saving to", filename, "was successfull.")

            self.has_been_modified = False


    def loadFromFile(self, filename):
        with open(filename, "r") as file:
            raw_data = file.read()
            try:
                data = json.loads(raw_data)
                self.deserialize(data)
                self.has_been_modified = False
            except json.JSONDecodeError:
                raise InvalidFile("%s is not a valid JSON file" % os.path.basename(filename))
            except Exception as e:
                dumpException(e)

    def setNodeClassSelector(self, class_selecting_function):
        self.node_class_selector = class_selecting_function

    def getNodeClassFromData(self, data):
        return Node if self.node_class_selector is None else self.node_class_selector(data)


    def serialize(self):
        nodes, edges = [], []
        for node in self.nodes: nodes.append(node.serialize())
        for edge in self.edges: edges.append(edge.serialize())
        return OrderedDict([
            ('id', self.id),
            ('scene_width', self.scene_width),
            ('scene_height', self.scene_height),
            ('nodes', nodes),
            ('edges', edges),
        ])

    def deserialize(self, data, hashmap={}, restore_id=True):
        print("deserializating data", data)

        self.clear()
        hashmap = {}
        if restore_id: self.id = data['id']


        # create nodes
        for node_data in data['nodes']:
            self.getNodeClassFromData(node_data)(self).deserialize(node_data, hashmap, restore_id)


        # create edges
        for edge_data in data['edges']:
            Edge(self).deserialize(edge_data, hashmap, restore_id)


        return True

