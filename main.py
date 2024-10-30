from PyQt5.QtWidgets import *
import sys
from pytomate_window import PytomateWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PytomateWindow()
    sys.exit(app.exec_())
    # If you want to app to run on both PyQt4 and PyQt5 then you need sys.exit(app.exec_())
    # otherwise app.exec_() is sufficient. Also app.exec() and app.exec_() are interchangeable.
