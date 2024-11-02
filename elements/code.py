from pytomate_conf import *
from pytomate_tool_base import *
from pytomate_content_widget import OurNodeContentWidget
from pytomate_utils import dumpException

class code_content(OurNodeContentWidget):
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