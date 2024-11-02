from PyQt5.QtWidgets import *
from pytomate_node import Node
from pytomate_content_widget import OurNodeContentWidget
from pytomate_graphics_node import OurGraphicsNode
from pytomate_utils import dumpException

class MdiGraphicsNode(OurGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 150
        self.height = 200
        self.edge_size = 8
        self._padding = 8


class MdiContent(OurNodeContentWidget):
    def initUI(self):
        lbl = QLabel(self.node.content_label, self)
        lbl.setObjectName(self.node.content_label_objname)


class MdiNode(Node):
    icon = ""
    op_code = 0
    op_title = "Undefined"
    content_label = ""
    content_label_objname = "tool_node_bg"

    def __init__(self, scene, inputs=[2, 2], outputs=[1]):
        super().__init__(scene, self.__class__.op_title, inputs, outputs)

    def initInnerClasses(self):
        self.content = MdiContent(self)
        self.grNode = MdiGraphicsNode(self)

    def evalImplementation(self):
        return 123

    def eval(self):
        try
            return self.evalImplementation()
        except Exception as e:
            dumpException(e)


    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        print("Deserialized CalcNode '%s'" % self.__class__.__name__, "res:", res)
        return res
