import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pytomate_window import PytomateWindow
from pytomate_sub_window import PytomateSubWindow
from pytomate_utils import dumpException, pp
from pytomate_draglist import OurDragListBox
from pytomate_conf import *

DEBUG = False

class PytomateMdiWindow(PytomateWindow):

    def initUI(self):
        self.name_company = 'Pytomate'
        self.name_product = 'Pytomate'

        self.empty_icon = QIcon(".")

        if DEBUG:
            print("Registered elements:")
            pp(TOOL_NODES)

        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setViewMode(QMdiArea.TabbedView)
        self.mdiArea.setDocumentMode(True)
        self.mdiArea.setTabsClosable(True)
        self.mdiArea.setTabsMovable(True)
        self.setCentralWidget(self.mdiArea)

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)

        self.createElementDock()
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()


        self.readSettings()

        self.setWindowTitle("Pytomate")

        self.createMdiWelcome()

    def closeEvent(self, event):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()


    def createActions(self):
        super().createActions()

        self.actClose = QAction("Cl&ose", self, statusTip="Close the active window", triggered=self.mdiArea.closeActiveSubWindow)
        self.actCloseAll = QAction("Close &All", self, statusTip="Close all the windows", triggered=self.mdiArea.closeAllSubWindows)
        self.actTile = QAction("&Tile", self, statusTip="Tile the windows", triggered=self.mdiArea.tileSubWindows)
        self.actCascade = QAction("&Cascade", self, statusTip="Cascade the windows", triggered=self.mdiArea.cascadeSubWindows)
        self.actNext = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild, statusTip="Move the focus to the next window", triggered=self.mdiArea.activateNextSubWindow)
        self.actPrevious = QAction("Pre&vious", self, shortcut=QKeySequence.PreviousChild, statusTip="Move the focus to the previous window", triggered=self.mdiArea.activatePreviousSubWindow)

        self.actSeparator = QAction(self)
        self.actSeparator.setSeparator(True)

        self.actAbout = QAction("&About", self, statusTip="Show the application's About box", triggered=self.about)

    def getCurrentNodeEditorWidget(self):
        """ we're returning NodeEditorWidget here... """
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None


    def onFileNew(self):
        try:
            subwnd = self.createMdiChild()
            subwnd.widget().fileNew()
            subwnd.show()
        except Exception as e: dumpException(e)

    def onFileOpen(self):
        fnames, filter = QFileDialog.getOpenFileNames(self, 'Open graph from file')

        try:
            for fname in fnames:
                if fname:
                    existing = self.findMdiChild(fname)
                    if existing:
                        self.mdiArea.setActiveSubWindow(existing)
                    else:
                        # we need to create new subWindow and open the file
                        pytomate = PytomateSubWindow()
                        if pytomate.fileLoad(fname):
                            self.statusBar().showMessage("File %s loaded" % fname, 5000)
                            pytomate.setTitle()
                            subwnd = self.mdiArea.addSubWindow(pytomate)
                            subwnd.show()
                        else:
                            pytomate.close()
        except Exception as e: dumpException(e)




    def about(self):
        QMessageBox.about(self, "About Pytomate",
                          "<b>Pytomate</b> is a tool designed to simplify automation with Python. "
                          "It features a flow builder that allows you to create custom automation workflows, "
                          "and it also provides pre-made modules for quick and easy automation solutions. "
                          "<br> <br> <b> Made By : Prashant Shukla <b> ")

    def createMenus(self):
        super().createMenus()

        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.actAbout)

        self.editMenu.aboutToShow.connect(self.updateEditMenu)


    def updateMenus(self):
        #print("update Menus")
        active = self.getCurrentNodeEditorWidget()
        hasMdiChild = (active is not None)

        self.actSave.setEnabled(hasMdiChild)
        self.actSaveAs.setEnabled(hasMdiChild)
        self.actClose.setEnabled(hasMdiChild)
        self.actCloseAll.setEnabled(hasMdiChild)
        self.actTile.setEnabled(hasMdiChild)
        self.actCascade.setEnabled(hasMdiChild)
        self.actNext.setEnabled(hasMdiChild)
        self.actPrevious.setEnabled(hasMdiChild)
        self.actSeparator.setVisible(hasMdiChild)

        self.updateEditMenu()

    def updateEditMenu(self):
        try:
            print("update Edit Menu")
            active = self.getCurrentNodeEditorWidget()
            hasMdiChild = (active is not None)

            self.actPaste.setEnabled(hasMdiChild)

            self.actCut.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actCopy.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actDelete.setEnabled(hasMdiChild and active.hasSelectedItems())

            self.actUndo.setEnabled(hasMdiChild and active.canUndo())
            self.actRedo.setEnabled(hasMdiChild and active.canRedo())
        except Exception as e: dumpException(e)

    def updateWindowMenu(self):
        self.windowMenu.clear()

        toolbar_elements = self.windowMenu.addAction("Elements Toolbar")
        toolbar_elements.setCheckable(True)
        toolbar_elements.triggered.connect(self.onWindowNodesToolbar)
        toolbar_elements.setChecked(self.elementsDock.isVisible())

        self.windowMenu.addSeparator()



        self.windowMenu.addAction(self.actClose)
        self.windowMenu.addAction(self.actCloseAll)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actTile)
        self.windowMenu.addAction(self.actCascade)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actNext)
        self.windowMenu.addAction(self.actPrevious)
        self.windowMenu.addAction(self.actSeparator)

        windows = self.mdiArea.subWindowList()
        self.actSeparator.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.getUserFriendlyFilename())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.getCurrentNodeEditorWidget())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def onWindowNodesToolbar(self):
        if self.elementsDock.isVisible():
            self.elementsDock.hide()
        else:
            self.elementsDock.show()


    def createToolBars(self):
        pass

    def createElementDock(self):
        self.elementsListWidget = OurDragListBox()

        self.elementsDock = QDockWidget("Elements")
        self.elementsDock.setWidget(self.elementsListWidget)
        self.elementsDock.setFloating(False)

        self.addDockWidget(Qt.RightDockWidgetArea, self.elementsDock)


    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createMdiChild(self, child_widget=None):
        pytomate = child_widget if child_widget is not None else PytomateSubWindow()
        subwnd = self.mdiArea.addSubWindow(pytomate)
        subwnd.setWindowIcon(self.empty_icon)
        pytomate.Scene.history.addHistoryModifiedListener(self.updateEditMenu)
        pytomate.addCloseEventListener(self.onSubWndClose)
        return subwnd

    def onSubWndClose(self, widget, event):
        existing = self.findMdiChild(widget.filename)
        self.mdiArea.setActiveSubWindow(existing)

        if self.maybeSave():
            event.accept()
        else:
            event.ignore()


    def findMdiChild(self, filename):
        for window in self.mdiArea.subWindowList():
            if window.widget().filename == filename:
                return window
        return None


    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)

    def createMdiWelcome(self):
        filename = "AmazonScrap"
        current_dir = os.getcwd()
        fname = os.path.join(current_dir, filename)
        if fname:
            existing = self.findMdiChild(fname)
            if existing:
                self.mdiArea.setActiveSubWindow(existing)
            else:
                pytomate = PytomateSubWindow()
                if pytomate.fileLoad(fname):
                    self.statusBar().showMessage("File %s loaded" % fname, 5000)
                    pytomate.setTitle()
                    subwnd = self.mdiArea.addSubWindow(pytomate)
                    subwnd.show()
                else:
                    pytomate.close()