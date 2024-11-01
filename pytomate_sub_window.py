from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pytomate_conf import *
from pytomate_widget import PytomateWidget
from pytomate_node import Node


class PytomateSubWindow(PytomateWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setTitle()

        self.Scene.addHasBeenModifiedListener(self.setTitle)
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
        # print("CalcSubWnd :: ~onDragEnter")
        # print("text: '%s'" % event.mimeData().text())
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            event.acceptProposedAction()
        else:
            # print(" ... denied drag enter event")
            event.setAccepted(False)

    def onDrop(self, event):
        # print("CalcSubWnd :: ~onDrop")
        # print("text: '%s'" % event.mimeData().text())
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            eventData = event.mimeData().data(LISTBOX_MIMETYPE)
            dataStream = QDataStream(eventData, QIODevice.ReadOnly)
            pixmap = QPixmap()
            dataStream >> pixmap
            op_code = dataStream.readInt()
            text = dataStream.readQString()

            mouse_position = event.pos()
            scene_position = self.Scene.graphicsScene.views()[0].mapToScene(mouse_position)

            print("GOT DROP: [%d] '%s'" % (op_code, text), "mouse:", mouse_position, "scene:", scene_position)


            node = Node(self.Scene, text, inputs=[1,1], outputs=[2])
            node.setPos(scene_position.x(), scene_position.y())
            self.Scene.addNode(node)


            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            # print(" ... drop ignored, not requested format '%s'" % LISTBOX_MIMETYPE)
            event.ignore()
