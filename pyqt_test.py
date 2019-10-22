import sys, os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox,
    QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGridLayout, QLabel, QLineEdit, QTextEdit)
from PyQt5.QtWidgets import QMainWindow, QAction, QLCDNumber, QSlider,QInputDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import serial

class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Message box')
        # self.buttonLayout()
        # self.gridLayout_Calculator()
        # self.gridLayout_Review()
        # self.slider_show()
        self.Dialog_show()
        self.center()
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        qr = self.frameGeometry()

        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def buttonLayout(self):
        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def gridLayout_Calculator(self):
        grid = QGridLayout()
        self.setLayout(grid)

        names = ['Cls', 'Bck', '', 'Close',
                 '7', '8', '9', '/',
                 '4', '5', '6', '*',
                 '1', '2', '3', '-',
                 '0', '.', '=', '+']

        positions = [(i, j) for i in range(5) for j in range(4)]

        for position, name in zip(positions, names):
            if name == '':
                continue
            button = QPushButton(name)
            grid.addWidget(button, *position)

    def gridLayout_Review(self):
        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('Review')

        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)

        grid.addWidget(review, 3, 0)
        grid.addWidget(reviewEdit, 3, 1, 5, 1)

        self.setLayout(grid)

    def slider_show(self):
        lcd = QLCDNumber(self)
        sld = QSlider(Qt.Horizontal, self)
        vbox = QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(sld)

        self.setLayout(vbox)
        sld.valueChanged.connect(lcd.display)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')
        if ok:
            self.le.setText(str(text))

    def Dialog_show(self):
        btn = QPushButton('Dialog', self)
        btn.move(20, 20)
        btn.clicked.connect(self.showDialog)
        self.le = QLineEdit(self)
        self.le.move(130, 22)


class Communicate(QObject):
    closeApp = pyqtSignal()


class Example2(QMainWindow):
    def __init__(self):
        super(Example2, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Message box')
        # self.menubar_show()
        self.btn_show()
        self.signal_show()
        self.center()
        self.show()

    def menubar_show(self):
        text_edit = QTextEdit()
        self.setCentralWidget(text_edit)

        exit_action = QAction(QIcon('app.ico'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exit_action)
        self.statusBar()

        menubar = self.menuBar()
        file_Menu = menubar.addMenu('&File')
        file_Menu.addAction(exit_action)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        qr = self.frameGeometry()

        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + 'was pressed')

    def btn_show(self):
        btn1 = QPushButton("Button 1", self)
        btn1.move(30, 50)

        btn2 = QPushButton("Button 2", self)
        btn2.move(150, 50)

        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)

        self.statusBar()

    def signal_show(self):
        self.conn = Communicate()
        self.conn.closeApp.connect(self.close)

    def mousePressEvent(self, event):
        self.conn.closeApp.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
