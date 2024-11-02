from PyQt5.QtGui import QFont
from pytomate_conf import *
from pytomate_tool_base import *
from pytomate_content_widget import OurNodeContentWidget

class exec_content(OurNodeContentWidget):
    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        self.exec = QLabel("Execute Code ", self)
        self.exec.setFont(QFont('Times', 10))
        self.layout.addWidget(self.exec)
        self.exec.setObjectName(self.node.content_label_objname)

class exec_graphics(MdiGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 150
        self.height = 80
        self.edge_size = 8
        self._padding = 8

@register_node(OP_NODE_EXEC)
class ToolNode_Exec(MdiNode):
    icon = "icons/exec.png"
    op_code = OP_NODE_EXEC
    op_title = "Exec"
    content_label = ""
    content_label_objname = "tool_node_ex"
    def __init__(self, scene):
        super().__init__(scene, inputs=[1,2,3], outputs=[3])

    def initInnerClasses(self):
        self.content = exec_content(self)
        self.grNode = exec_graphics(self)