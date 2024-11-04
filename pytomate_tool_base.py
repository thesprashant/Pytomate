from PyQt5.QtGui import *
from PyQt5.QtCore import *
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

    def initAssets(self):
        super().initAssets()
        self.icons = QImage("icons/status_icons.png")

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)

        offset = 24.0
        if self.node.isDirty(): offset = 0.0
        if self.node.isInvalid(): offset = 48.0

        painter.drawImage(
            QRectF(-10, -10, 24.0, 24.0),
            self.icons,
            QRectF(offset, 0, 24.0, 24.0)
        )


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

        self.value = None
        self.markDirty()

    def initInnerClasses(self):
        self.content = MdiContent(self)
        self.grNode = MdiGraphicsNode(self)

    def evalImplementation(self):
        return 123

    def eval(self):
        if not self.isDirty() and not self.isInvalid():
            print(" _> returning cached %s value:" % self.__class__.__name__, self.value)
            return self.value

        try:

            val = self.evalImplementation()
            print("eval executed")
            return val

        except Exception as e:
            self.markInvalid()
            dumpException(e)



    def onInputChanged(self, new_edge):
        print("%s::__onInputChanged" % self.__class__.__name__)
        self.markDirty()
        self.eval()

    def onChecked(self):
        print("%s::__onChecked" % self.__class__.__name__)
        self.evalImplementation()


    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        print("Deserialized CalcNode '%s'" % self.__class__.__name__, "res:", res)
        return res
