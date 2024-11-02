from pytomate_conf import *
from PyQt5.QtCore import *
from pytomate_tool_base import *
from pytomate_content_widget import OurNodeContentWidget
from pytomate_utils import dumpException

class result_content(OurNodeContentWidget):
    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        self.edit = QTextEdit("", self)
        self.layout.addWidget(self.edit)
        self.edit.setPlaceholderText("Result will be shown here ")
        self.edit.setReadOnly(True)
        self.edit.setAlignment(Qt.AlignLeft)
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

@register_node(OP_NODE_RESULT)
class ToolNode_Result(MdiNode):
    icon = "icons/result.png"
    op_code = OP_NODE_RESULT
    op_title = "Result"
    content_label = ""
    content_label_objname = "tool_node_re"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1,2,3], outputs=[3])

    def initInnerClasses(self):
        self.content = result_content(self)
        self.grNode = MdiGraphicsNode(self)
