import os
from PyQt5.QtWidgets import *
from pytomate_widget import PytomateWidget


class PytomateWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.filename = None


    def createAct(self, name, shortcut, tooltip, callback):
        act = QAction(name, self)
        act.setShortcut(shortcut)
        act.setToolTip(tooltip)
        act.triggered.connect(callback)
        return act

    def initUI(self):
        menubar = self.menuBar()

        # initialize Menu
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.createAct('&New', 'Ctrl+N', "Create new automation", self.onFileNew))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAct('&Open', 'Ctrl+O', "Open file", self.onFileOpen))
        fileMenu.addAction(self.createAct('&Save', 'Ctrl+S', "Save file", self.onFileSave))
        fileMenu.addAction(self.createAct('Save &As...', 'Ctrl+Shift+S', "Save file as...", self.onFileSaveAs))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAct('E&xit', 'Ctrl+Q', "Exit application", self.close))

        editMenu = menubar.addMenu('&Edit')
        editMenu.addAction(self.createAct('&Delete', 'Del', "Delete selected items", self.onEditDelete))

        pytomate = PytomateWidget(self)
        self.setCentralWidget(pytomate)

        self.statusBar().showMessage("")
        self.status_mouse_pos = QLabel("")
        self.statusBar().addPermanentWidget(self.status_mouse_pos)
        pytomate.view.scenePosChanged.connect(self.onScenePosChanged)


        self.setGeometry(300, 150, 1280, 720)
        self.setWindowTitle("Pytomate")
        self.show()

    def onScenePosChanged(self, x, y):
        self.status_mouse_pos.setText("Scene Pos: [%d, %d]" % (x, y))

    def onFileNew(self):
        self.centralWidget().Scene.clear()

    def onFileOpen(self):
        fname, filter = QFileDialog.getOpenFileName(self, 'Open graph from file')
        if fname == '':
            return
        if os.path.isfile(fname):
            self.centralWidget().Scene.loadFromFile(fname)

    def onFileSave(self):
        if self.filename is None: return self.onFileSaveAs()
        self.centralWidget().Scene.saveToFile(self.filename)
        self.statusBar().showMessage("Successfully saved %s" % self.filename)

    def onFileSaveAs(self):
        fname, filter = QFileDialog.getSaveFileName(self, 'Save graph to file')
        if fname == '':
            return
        self.filename = fname
        self.onFileSave()

    def onEditDelete(self):
        self.centralWidget().Scene.graphicsScene.views()[0].deleteSelected(self)
