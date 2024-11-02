from pytomate_conf import *
from pytomate_tool_base import *
from pytomate_content_widget import OurNodeContentWidget
from pytomate_utils import dumpException

class note_content(OurNodeContentWidget):
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