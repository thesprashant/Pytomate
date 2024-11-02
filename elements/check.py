from pytomate_conf import *
from pytomate_tool_base import *
from pytomate_content_widget import OurNodeContentWidget
from pytomate_utils import dumpException

class check_content(OurNodeContentWidget):
    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        self.check = QCheckBox(self)
        self.layout.addWidget(self.check)
        self.check.setObjectName(self.node.content_label_objname)
    def serialize(self):
        res = super().serialize()
        res['value'] = self.check.isChecked()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.check.setChecked(value)
            return True & res
        except Exception as e:
            dumpException(e)
        return res

class check_graphics(MdiGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 80
        self.height = 80
        self.edge_size = 8
        self._padding = 8

@register_node(OP_NODE_CHECK)
class ToolNode_Check(MdiNode):
    icon = "icons/check.png"
    op_code = OP_NODE_CHECK
    op_title = "Switch"
    content_label = ""
    content_label_objname = "tool_node_ch"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1,2,3], outputs=[3])

    def initInnerClasses(self):
        self.content = check_content(self)
        self.grNode = check_graphics(self)