import os
import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pytomate_widget import PytomateWidget



class PytomateWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.name_company = 'Pytomate'
        self.name_product = 'Pytomate'

        self.initUI()

    def initUI(self):
        self.createActions()
        self.createMenus()


        self.pytomate = PytomateWidget(self)
        self.pytomate.Scene.addHasBeenModifiedListener(self.setTitle)
        self.setCentralWidget(self.pytomate)

        self.createStatusBar()

        self.setGeometry(300, 150, 1280, 720)
        self.setTitle()
        self.show()

    def createStatusBar(self):
        self.statusBar().showMessage("")
        self.status_mouse_pos = QLabel("")
        self.statusBar().addPermanentWidget(self.status_mouse_pos)
        self.nodeeditor.view.scenePosChanged.connect(self.onScenePosChanged)

    def createActions(self):
        self.actNew = QAction('&New', self, shortcut='Ctrl+N', statusTip="Create new Automation", triggered=self.onFileNew)
        self.actOpen = QAction('&Open', self, shortcut='Ctrl+O', statusTip="Open file", triggered=self.onFileOpen)
        self.actSave = QAction('&Save', self, shortcut='Ctrl+S', statusTip="Save file", triggered=self.onFileSave)
        self.actSaveAs = QAction('Save &As...', self, shortcut='Ctrl+Shift+S', statusTip="Save file as...", triggered=self.onFileSaveAs)
        self.actExit = QAction('E&xit', self, shortcut='Ctrl+Q', statusTip="Exit application", triggered=self.close)

        self.actUndo = QAction('&Undo', self, shortcut='Ctrl+Z', statusTip="Undo last operation", triggered=self.onEditUndo)
        self.actRedo = QAction('&Redo', self, shortcut='Ctrl+Shift+Z', statusTip="Redo last operation", triggered=self.onEditRedo)
        self.actCut = QAction('Cu&t', self, shortcut='Ctrl+X', statusTip="Cut to clipboard", triggered=self.onEditCut)
        self.actCopy = QAction('&Copy', self, shortcut='Ctrl+C', statusTip="Copy to clipboard", triggered=self.onEditCopy)
        self.actPaste = QAction('&Paste', self, shortcut='Ctrl+V', statusTip="Paste from clipboard", triggered=self.onEditPaste)
        self.actDelete = QAction('&Delete', self, shortcut='Del', statusTip="Delete selected items", triggered=self.onEditDelete)


    def createMenus(self):
        menubar = self.menuBar()

        self.fileMenu = menubar.addMenu('&File')
        self.fileMenu.addAction(self.actNew)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actOpen)
        self.fileMenu.addAction(self.actSave)
        self.fileMenu.addAction(self.actSaveAs)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actExit)

        self.editMenu = menubar.addMenu('&Edit')
        self.editMenu.addAction(self.actUndo)
        self.editMenu.addAction(self.actRedo)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.actCut)
        self.editMenu.addAction(self.actCopy)
        self.editMenu.addAction(self.actPaste)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.actDelete)


    def setTitle(self):
        title = "Node Editor - "
        title += self.getCurrentNodeEditorWidget().getUserFriendlyFilename()

        self.setWindowTitle(title)


    def closeEvent(self, event):
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def isModified(self):
        return self.getCurrentNodeEditorWidget().Scene.isModified()


    def getCurrentNodeEditorWidget(self):
        return self.centralWidget()

    def maybeSave(self):
        if not self.isModified():
            return True

        res = QMessageBox.warning(self, "About to loose your work?",
                "The document has been modified.\n Do you want to save your changes?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
              )

        if res == QMessageBox.Save:
            return self.onFileSave()
        elif res == QMessageBox.Cancel:
            return False

        return True



    def onScenePosChanged(self, x, y):
        self.status_mouse_pos.setText("Scene Pos: [%d, %d]" % (x, y))

    def onFileNew(self):
        if self.maybeSave():
            self.getCurrentNodeEditorWidget().fileNew()
            self.setTitle()


    def onFileOpen(self):
        if self.maybeSave():
            fname, filter = QFileDialog.getOpenFileName(self, 'Open automation graph from file')
            if fname != '' and os.path.isfile(fname):
                self.getCurrentNodeEditorWidget().fileLoad(fname)
                self.setTitle()

    def onFileSave(self):
        current_pytomate = self.getCurrentNodeEditorWidget()
        if current_pytomate is not None:
            if not current_pytomate.isFilenameSet(): return self.onFileSaveAs()

            current_pytomate.fileSave()
            self.statusBar().showMessage("Successfully saved %s" % current_pytomate.filename, 5000)

            # support for MDI app
            if hasattr(current_pytomate, "setTitle"): current_pytomate.setTitle()
            else: self.setTitle()
            return True


    def onFileSaveAs(self):
        current_pytomate = self.getCurrentNodeEditorWidget()
        if current_pytomate is not None:
            fname, filter = QFileDialog.getSaveFileName(self, 'Save graph to file')
            if fname == '': return False

            current_pytomate.fileSave(fname)
            self.statusBar().showMessage("Successfully saved as %s" % current_pytomate.filename, 5000)

            # support for MDI app
            if hasattr(current_pytomate, "setTitle"): current_pytomate.setTitle()
            else: self.setTitle()
            return True



    def onEditUndo(self):
        if self.getCurrentNodeEditorWidget():
            self.getCurrentNodeEditorWidget().Scene.history.undo()


    def onEditRedo(self):
        if self.getCurrentNodeEditorWidget():
            self.getCurrentNodeEditorWidget().Scene.history.redo()


    def onEditDelete(self):
        if self.getCurrentNodeEditorWidget():
            self.getCurrentNodeEditorWidget().Scene.getView().deleteSelected(self)



    def onEditCut(self):
        if self.getCurrentNodeEditorWidget():
            data = self.getCurrentNodeEditorWidget().Scene.clipboard.serializeSelected(delete=True)
            str_data = json.dumps(data, indent=4)
            QApplication.instance().clipboard().setText(str_data)

    def onEditCopy(self):
        if self.getCurrentNodeEditorWidget():
            data = self.getCurrentNodeEditorWidget().Scene.clipboard.serializeSelected(delete=False)
            str_data = json.dumps(data, indent=4)
            QApplication.instance().clipboard().setText(str_data)

    def onEditPaste(self):
        if self.getCurrentNodeEditorWidget():
            raw_data = QApplication.instance().clipboard().text()

            try:
                data = json.loads(raw_data)
            except ValueError as e:
                print("Pasting of not valid json data!", e)
                return

            # check if the json data are correct
            if 'nodes' not in data:
                print("JSON does not contain any nodes!")
                return

            self.getCurrentNodeEditorWidget().Scene.clipboard.deserializeFromClipboard(data)

    def readSettings(self):
        settings = QSettings(self.name_company, self.name_product)
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(400, 400))
        self.move(pos)
        self.resize(size)

    def writeSettings(self):
        settings = QSettings(self.name_company, self.name_product)
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())
