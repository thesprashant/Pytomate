from pytomate_conf import *
from pytomate_tool_base import *


@register_node(OP_NODE_SWITCH)
class ToolNode_Switch(MdiNode):
    icon = "icons/switch.png"
    op_code = OP_NODE_SWITCH
    op_title = "Switch"
    content_label = ""

@register_node(OP_NODE_NOTE)
class ToolNode_Note(MdiNode):
    icon = "icons/note.png"
    op_code = OP_NODE_NOTE
    op_title = "Note"
    content_label = ""


@register_node(OP_NODE_RESULT)
class ToolNode_Result(MdiNode):
    icon = "icons/result.png"
    op_code = OP_NODE_RESULT
    op_title = "Result"
    content_label = ""


@register_node(OP_NODE_EXEC)
class ToolNode_Exec(MdiNode):
    icon = "icons/exec.png"
    op_code = OP_NODE_EXEC
    op_title = "Exec"
    content_label = ""


@register_node(OP_NODE_INPUT)
class ToolNode_Input(MdiNode):
    icon = "icons/in.png"
    op_code = OP_NODE_INPUT
    op_title = "Input"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[3])

@register_node(OP_NODE_OUTPUT)
class ToolNode_Output(MdiNode):
    icon = "icons/out.png"
    op_code = OP_NODE_OUTPUT
    op_title = "Output"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[])
