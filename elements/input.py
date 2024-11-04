from pytomate_conf import *
from PyQt5.QtCore import *
from pytomate_tool_base import *
from pytomate_content_widget import OurNodeContentWidget
from pytomate_utils import dumpException

class input_content(OurNodeContentWidget):
    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        self.edit = MyTextEdit()
        self.edit.setPlaceholderText("Enter Input: ")
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

class input_graphics(MdiGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 200
        self.height = 150
        self.edge_size = 8
        self._padding = 8

class MyTextEdit(QTextEdit):
    plainTextChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.textChanged.connect(self.emitPlainTextChanged)

    def emitPlainTextChanged(self):
        self.plainTextChanged.emit(self.toPlainText())

@register_node(OP_NODE_INPUT)
class ToolNode_Input(MdiNode):
    icon = "icons/in.png"
    op_code = OP_NODE_INPUT
    op_title = "Input"
    content_label_objname = "tool_node_in"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[3])
        self.eval()

    def initInnerClasses(self):
        self.content = input_content(self)
        self.grNode = input_graphics(self)
        self.content.edit.plainTextChanged.connect(self.onInputChanged)


    def handleTextChanged(self):
        self.content.edit.emit(self.toPlainText())
        self.onInputChanged()

    def evalImplementation(self):
        self.value = self.content.edit.toPlainText()
        self.markDirty(False)
        self.markInvalid(False)
        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()
        self.evalChildren()
        return self.value