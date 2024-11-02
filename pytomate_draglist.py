from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from pytomate_conf import *
from pytomate_utils import dumpException


class OurDragListBox(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):

        self.setIconSize(QSize(32, 32))
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)

        self.addMyItems()

    def addMyItems(self):
        self.addMyItem("Input", "icons/in.png", OP_NODE_INPUT)
        self.addMyItem("Output", "icons/out.png", OP_NODE_OUTPUT)
        self.addMyItem("Exec", "icons/exec.png", OP_NODE_EXEC)
        self.addMyItem("Result", "icons/result.png", OP_NODE_RESULT)
        self.addMyItem("Note", "icons/note.png", OP_NODE_NOTE)

    def addMyItem(self, name, icon=None, op_code=0):
        item = QListWidgetItem(name, self)  # can be (icon, text, parent, <int>type)
        pixmap = QPixmap(icon if icon is not None else ".")
        item.setIcon(QIcon(pixmap))
        item.setSizeHint(QSize(32, 32))

        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

        # setup data
        item.setData(Qt.UserRole, pixmap)
        item.setData(Qt.UserRole + 1, op_code)

    def startDrag(self, *args, **kwargs):
        # print("ListBox::startDrag")

        try:
            item = self.currentItem()
            op_code = item.data(Qt.UserRole + 1)
            # print("dragging item <%d>" % op_code, item)

            pixmap = QPixmap(item.data(Qt.UserRole))


            itemData = QByteArray()
            dataStream = QDataStream(itemData, QIODevice.WriteOnly)
            dataStream << pixmap
            dataStream.writeInt(op_code)
            dataStream.writeQString(item.text())

            mimeData = QMimeData()
            mimeData.setData(LISTBOX_MIMETYPE, itemData)

            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(QPoint(int(pixmap.width() / 2), int(pixmap.height() / 2)))
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)

        except Exception as e: dumpException(e)
