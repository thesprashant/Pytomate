from pytomate_conf import *
from pytomate_tool_base import *
from pytomate_content_widget import OurNodeContentWidget
from pytomate_utils import dumpException

class output_content(OurNodeContentWidget):
    def initUI(self):
        self.value = None
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        self.edit = QTextEdit("", self)
        self.edit.setPlaceholderText("Output ")
        self.edit.setReadOnly(True)
        self.edit.setAlignment(Qt.AlignLeft)
        self.layout.addWidget(self.edit)
        self.edit.setObjectName(self.node.content_label_objname)
    def serialize(self):
        res = super().serialize()
        res['value'] = self.edit.toPlainText()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.edit.setText(value)
            return True & res
        except Exception as e:
            dumpException(e)
        return res

class output_graphics(MdiGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 200
        self.height = 150
        self.edge_size = 8
        self._padding = 8

@register_node(OP_NODE_OUTPUT)
class ToolNode_Output(MdiNode):
    icon = "icons/out.png"
    op_code = OP_NODE_OUTPUT
    op_title = "Output"
    content_label_objname = "tool_node_ou"

    def __init__(self, scene):
        super().__init__(scene, inputs=[3], outputs=[])

    def initInnerClasses(self):
        self.content = output_content(self)
        self.grNode = output_graphics(self)

    def eval(self):
        try:

            val = self.evalImplementation()
            print("eval executed")
            return val

        except Exception as e:
            self.markInvalid()
            dumpException(e)

    def evalImplementation(self):
        input_node = self.getInput(0)
        if not input_node:
            self.markInvalid()
            return
        val = input_node.eval()
        self.value = val
        if not val:
            self.markInvalid()
            return
        self.content.edit.setText(val)
        self.markInvalid(False)
        self.markDirty(False)
        return val
