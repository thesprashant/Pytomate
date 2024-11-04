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
    pass

@register_node(OP_NODE_CODE)
class ToolNode_Code(MdiNode):
    icon = "icons/code.png"
    op_code = OP_NODE_CODE
    op_title = "Code"
    content_label_objname = "tool_node_co"


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

        print("code from input edge is: ")
        pattern = r'inputtocode = .*?(\n|$)'
        if "inputtocode = " in old_val:
            cleaned_val = re.sub(pattern, '', old_val)
            print("cleaned old value is: ",cleaned_val)
            val = val.rstrip('\n')
            new_val = "inputtocode = \'" + val + "\'"
            new_val = new_val.rstrip('\n')
            new_val = new_val + '\n' + cleaned_val
            print("new value is: ",new_val)
        else:
            #new_val = "inputtocode = \'" + val + "\'" +old_val
            new_val = "inputtocode = \'" + val + "\'"
            new_val = new_val.rstrip()
            new_val = new_val + '\n' + old_val
        # cursor = self.content.text.textCursor()
        # cursor.movePosition(QTextCursor.Start)
        # self.content.text.setTextCursor(cursor)
        self.value = new_val
        self.content.text.setText(new_val)
        self.markInvalid(False)
        self.markDirty(False)
        self.evalChildren()
        return self.value
