from pytomate_conf import *
from PyQt5.QtCore import *
from pytomate_tool_base import *
from pytomate_content_widget import OurNodeContentWidget

class check_content(OurNodeContentWidget):
    def initUI(self):
        self.check = QCheckBox(self)
        self.check.setObjectName(self.node.content_label_objname)

class check_graphics(MdiGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 100
        self.height = 100
        self.edge_size = 8
        self._padding = 8

@register_node(OP_NODE_CHECK)
class ToolNode_Check(MdiNode):
    icon = "icons/check.png"
    op_code = OP_NODE_CHECK
    op_title = "Check"
    content_label = ""
    content_label_objname = "tool_node_ch"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1,2,3], outputs=[3])

    def initInnerClasses(self):
        self.content = check_content(self)
        self.grNode = check_graphics(self)

class note_content(OurNodeContentWidget):
    pass

class note_graphics(OurGraphicsNode):
    pass

@register_node(OP_NODE_NOTE)
class ToolNode_Note(MdiNode):
    icon = "icons/note.png"
    op_code = OP_NODE_NOTE
    op_title = "Note"
    content_label = ""
    content_label_objname = "tool_node_no"
    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[1])

    def initInnerClasses(self):
        self.content = note_content(self)
        self.grNode = note_graphics(self)

class result_content(OurNodeContentWidget):
    def initUI(self):
        self.edit = QLineEdit("", self)
        self.edit.setPlaceholderText("Enter Input: ")
        self.edit.setReadOnly(True)
        self.edit.setAlignment(Qt.AlignLeft)
        self.edit.setObjectName(self.node.content_label_objname)

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

class exec_content(OurNodeContentWidget):
    def initUI(self):
        self.exec = QLabel(" ", self)
        self.exec.setObjectName(self.node.content_label_objname)

class exec_graphics(MdiGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 150
        self.height = 150
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

class input_content(OurNodeContentWidget):
    def initUI(self):
        self.edit = QLineEdit("", self)
        self.edit.setPlaceholderText("Enter Input: ")
        self.edit.setAlignment(Qt.AlignLeft)
        self.edit.setObjectName(self.node.content_label_objname)


@register_node(OP_NODE_INPUT)
class ToolNode_Input(MdiNode):
    icon = "icons/in.png"
    op_code = OP_NODE_INPUT
    op_title = "Input"
    content_label_objname = "tool_node_in"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[3])

    def initInnerClasses(self):
        self.content = input_content(self)
        self.grNode = MdiGraphicsNode(self)


@register_node(OP_NODE_OUTPUT)
class ToolNode_Output(MdiNode):
    icon = "icons/out.png"
    op_code = OP_NODE_OUTPUT
    op_title = "Output"
    content_label_objname = "tool_node_ou"


    def __init__(self, scene):
        super().__init__(scene, inputs=[3], outputs=[])

class code_content(OurNodeContentWidget):
    pass

class code_graphics(OurGraphicsNode):
    pass

@register_node(OP_NODE_CODE)
class ToolNode_Code(MdiNode):
    icon = "icons/code.png"
    op_code = OP_NODE_CODE
    op_title = "Code"
    content_label_objname = "tool_node_co"


    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[2])

    def initInnerClasses(self):
        self.content = code_content(self)
        self.grNode = code_graphics(self)