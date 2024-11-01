import os
from PyQt5.QtWidgets import *
import sys
from pytomate_mdi_window import PytomateMdiWindow

sys.path.insert(0, os.path.join( os.path.dirname(__file__), "..", ".." ))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PytomateMdiWindow()
    window.show()
    sys.exit(app.exec_())
    # If you want to app to run on both PyQt4 and PyQt5 then you need sys.exit(app.exec_())
    # otherwise app.exec_() is sufficient. Also app.exec() and app.exec_() are interchangeable.