from test_designer import Ui_MainWindow
from PyQt5 import QtWidgets
from ui_func_code import UI_Func
import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = UI_Func()
    ui.show()
    sys.exit(app.exec_())
