import re
from pytomate_conf import *
from pytomate_tool_base import *
from pytomate_content_widget import OurNodeContentWidget
from pytomate_utils import dumpException

class code_content(OurNodeContentWidget):
    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        self.wdg_label = QLineEdit()
        self.wdg_label.setPlaceholderText("Title")
        self.layout.addWidget(self.wdg_label)
        self.text=QTextEdit()
        self.text.setPlaceholderText("Enter Code: ")
        self.layout.addWidget(self.text)

    def serialize(self):
        res = super().serialize()
        res['value0'] = self.wdg_label.text()
        res['value1'] = self.text.toPlainText()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value0 = data['value0']
            value1 = data['value1']
            self.wdg_label.setText(value0)
            self.text.setText(value1)
            return True & res
        except Exception as e:
            dumpException(e)
        return res


class code_graphics(OurGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 300
        self.height = 180
        self.edge_size = 8
        self._padding = 8

@register_node(OP_NODE_CODENORM)
class ToolNode_CodeNorm(MdiNode):
    icon = "icons/code.png"
    op_code = OP_NODE_CODENORM
    op_title = "Normal Code"
    content_label_objname = "tool_node_cod"


    def __init__(self, scene):
        super().__init__(scene, inputs=[3], outputs=[3])

    def initInnerClasses(self):
        self.content = code_content(self)
        self.grNode = code_graphics(self)

    def evalImplementation(self):
        old_val = self.content.text.toPlainText()
        input_node = self.getInput(0)
        if not input_node:
            self.markInvalid()
            return
        val = input_node.eval()
        new_val = val + '\n' + old_val
        self.value = new_val
        #self.content.text.setText(val)
        self.markInvalid(False)
        self.markDirty(False)
        self.evalChildren()
        return self.value
