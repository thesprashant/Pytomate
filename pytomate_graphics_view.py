from platform import release

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from pytomate_graphics_socket import OurGraphicsSocket
from pytomate_graphics_edge import OurGraphicsEdge
from pytomate_edge import Edge, EDGE_TYPE_BEZIER




MODE_NOOP = 1
MODE_EDGE_DRAG = 2

EDGE_DRAG_START_THRESHOLD = 10

DEBUG = True


class OurQGraphicsView(QGraphicsView):
    scenePosChanged = pyqtSignal(int, int)

    def __init__(self, graphicsScene, parent=None):
        super().__init__(parent)
        self.graphicsScene = graphicsScene

        self.initui()

        self.mode = MODE_NOOP
        self.rubberBandDraggingRectangle = False

        self.zoomInFactor = 1.25
        self.zoomOutFactor = 1 / self.zoomInFactor
        self.zoom = 5
        self.zoomClamp = True
        self.zoomStep = 1
        self.zoomRange = [0, 10]

        self.setScene(self.graphicsScene)
    def initui(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)


    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    def middleMouseButtonPress(self, event):
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                   Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)

    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() & -Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    def leftMouseButtonPress(self, event):
        item = self.getItemAtClick(event)

        # we store the position of last LMB click
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())

        if hasattr(item, "node") or isinstance(item, OurGraphicsEdge):
            if event.modifiers() & Qt.ShiftModifier:
                if DEBUG: print("LMB + Shift on", item)
                event.ignore()
                fakeEvent = QMouseEvent(QEvent.MouseButtonPress, event.localPos(), event.screenPos(),
                                        Qt.LeftButton, event.buttons() | Qt.LeftButton,
                                        event.modifiers() | Qt.ControlModifier)
                super().mousePressEvent(fakeEvent)
                return

        # logic
        if type(item) is OurGraphicsSocket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return

        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item)
            if res: return

        if item is None:
            self.rubberBandDraggingRectangle = True

        super().mousePressEvent(event)

    def rightMouseButtonPress(self, event):
        super().mousePressEvent(event)

        item = self.getItemAtClick(event)

        if DEBUG:
            if isinstance(item, OurGraphicsEdge): print('RMB DEBUG:', item.edge, ' connecting sockets:',
                                            item.edge.start_socket, '<-->', item.edge.end_socket)
            if type(item) is OurGraphicsSocket: print('RMB DEBUG:', item.socket, 'has edges:', item.socket.edges)

            if item is None:
                print('SCENE:')
                print('  Nodes:')
                for node in self.graphicsScene.scene.nodes: print('    ', node)
                print('  Edges:')
                for edge in self.graphicsScene.scene.edges: print('    ', edge)


    def leftMouseButtonRelease(self, event):
        return super().mouseReleaseEvent(event)
        # get item which we release mouse button on
        item = self.getItemAtClick(event)

        if hasattr(item, "node") or isinstance(item, OurGraphicsEdge):
            if event.modifiers() & Qt.ShiftModifier:
                if DEBUG: print("LMB Release + Shift on", item)
                event.ignore()
                fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                        Qt.LeftButton, Qt.NoButton,
                                        event.modifiers() | Qt.ControlModifier)
                super().mouseReleaseEvent(fakeEvent)
                return

        # logic
        if self.mode == MODE_EDGE_DRAG:
            if self.distanceBetweenClickAndReleaseIsOff(event):
                res = self.edgeDragEnd(item)
                if res: return

        if self.rubberBandDraggingRectangle:
            self.graphicsScene.scene.history.storeHistory("Selection changed")
            self.rubberBandDraggingRectangle = False
        super().mouseReleaseEvent(event)



    def rightMouseButtonRelease(self, event):
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
            if self.mode == MODE_EDGE_DRAG:
                pos = self.mapToScene(event.pos())
                self.drag_edge.grEdge.setDestination(pos.x(), pos.y())
                self.drag_edge.grEdge.update()

            self.last_scene_mouse_position = self.mapToScene(event.pos())

            self.scenePosChanged.emit(
                int(self.last_scene_mouse_position.x()), int(self.last_scene_mouse_position.y())
            )

            super().mouseMoveEvent(event)

    def getItemAtClick(self, event):
        """ return the object on which we've clicked/release mouse button """
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj


    def edgeDragStart(self, item):
        if DEBUG: print('View::edgeDragStart ~   assign Start Socket to:', item.socket)
        self.drag_start_socket = item.socket
        self.drag_edge = Edge(self.graphicsScene.scene, item.socket, None, EDGE_TYPE_BEZIER)
        if DEBUG: print('View::edgeDragStart ~   dragEdge:', self.drag_edge)



    def edgeDragEnd(self, item):
        """ return True if skip the rest of the code """
        self.mode = MODE_NOOP

        if DEBUG: print('View::edgeDragEnd ~ End dragging edge')
        self.drag_edge.remove()
        self.drag_edge = None


        if type(item) is OurGraphicsSocket:
            if item.socket != self.drag_start_socket:
                for edge in item.socket.edges:
                    edge.remove()

                new_edge = Edge(self.graphicsScene.scene, self.drag_start_socket, item.socket, edge_type=EDGE_TYPE_BEZIER)
                if DEBUG: print("View::edgeDragEnd ~  created new edge: ", new_edge, "connecting", new_edge.start_socket, " <--> ", new_edge)
                self.graphicsScene.scene.history.storeHistory("Created new edge by dragging", setModified=True)
                return True

        if DEBUG: print('View::edgeDragEnd ~ everything done.')
        return False


    def distanceBetweenClickAndReleaseIsOff(self, event):
        """ measures if we are too far from the last LMB click scene position """
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        dist_scene = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        edge_drag_threshold_sq = EDGE_DRAG_START_THRESHOLD*EDGE_DRAG_START_THRESHOLD
        return (dist_scene.x()*dist_scene.x() + dist_scene.y()*dist_scene.y()) > edge_drag_threshold_sq

    def wheelEvent(self, event):

        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = self.zoomOutFactor
            self.zoom -= self.zoomStep

        clamped = False
        if self.zoom < self.zoomRange[0]: self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]: self.zoom, clamped = self.zoomRange[1], True

        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.deleteSelected(event)
        elif event.key() == Qt.Key_S and event.modifiers() & Qt.ControlModifier:
            self.graphicsScene.scene.saveToFile("graph.json.txt")
        elif event.key() == Qt.Key_L and event.modifiers() & Qt.ControlModifier:
            self.graphicsScene.scene.loadFromFile("graph.json.txt")
        elif event.key() == Qt.Key_Z and event.modifiers() & Qt.ControlModifier and not event.modifiers() & Qt.ShiftModifier:
            self.graphicsScene.scene.history.undo()
        elif event.key() == Qt.Key_Z and event.modifiers() & Qt.ControlModifier and event.modifiers() & Qt.ShiftModifier:
            self.graphicsScene.scene.history.redo()
        elif event.key() == Qt.Key_H:
            ix = 0
            for item in self.graphicsScene.scene.history.history_stack:
                print("#", ix, "--", item['desc'])
                ix += 1
        else:
            super().keyPressEvent(event)

    def deleteSelected(self, event):
        for item in self.graphicsScene.selectedItems():
            if isinstance(item, OurGraphicsEdge):
                item.edge.remove()
            elif hasattr(item, 'node'):
                item.node.remove()
        self.graphicsScene.scene.history.storeHistory("Delete selected", setModified=True)

    def debug_modifiers(self, event):
        out = "MODS: "
        if event.modifiers() & Qt.ShiftModifier: out += "SHIFT "
        if event.modifiers() & Qt.ControlModifier: out += "CTRL "
        if event.modifiers() & Qt.AltModifier: out += "ALT "
        return out

    def getItemAtClick(self, event):
        """ return the object on which we've clicked/release mouse button """
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

