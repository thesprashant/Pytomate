from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pytomate_conf import *
from pytomate_widget import PytomateWidget
from pytomate_node import Node
from pytomate_tool_base import *
from pytomate_conf import *
from pytomate_utils import dumpException


DEBUG = False

class PytomateSubWindow(PytomateWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setTitle()

        self.Scene.addHasBeenModifiedListener(self.setTitle)
        self._close_event_listeners = []

        self.Scene.addDragEnterListener(self.onDragEnter)
        self.Scene.addDropListener(self.onDrop)

        self._close_event_listeners = []


    def setTitle(self):
        self.setWindowTitle(self.getUserFriendlyFilename())

    def addCloseEventListener(self, callback):
        self._close_event_listeners.append(callback)

    def closeEvent(self, event):
        for callback in self._close_event_listeners: callback(self, event)

    def onDragEnter(self, event):
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            event.acceptProposedAction()
        else:
            # print(" ... denied drag enter event")
            event.setAccepted(False)

    def onDrop(self, event):
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            eventData = event.mimeData().data(LISTBOX_MIMETYPE)
            dataStream = QDataStream(eventData, QIODevice.ReadOnly)
            pixmap = QPixmap()
            dataStream >> pixmap
            op_code = dataStream.readInt()
            text = dataStream.readQString()

            mouse_position = event.pos()
            scene_position = self.Scene.graphicsScene.views()[0].mapToScene(mouse_position)

            if DEBUG: print("GOT DROP: [%d] '%s'" % (op_code, text), "mouse:", mouse_position, "scene:", scene_position)

            try:
                element = get_class_from_opcode(op_code)(self.Scene)
                element.setPos(scene_position.x(), scene_position.y())
                self.Scene.history.storeHistory("Created node %s" % element.__class__.__name__)
            except Exception as e: dumpException(e)



            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            # print(" ... drop ignored, not requested format '%s'" % LISTBOX_MIMETYPE)
            event.ignore()
