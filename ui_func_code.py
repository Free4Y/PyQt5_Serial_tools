# 由于pyinstaller 打包代码有问题，打包时找不到QtCore这个库
# 所以需要在UI文件转换成py文件之后，把以下代码拷贝到py文件的头部
# 在代码中强制引入PATH路径
import sys,os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import QtCore, QtGui, QtWidgets
from test_designer import Ui_MainWindow
import serial
import serial.tools.list_ports
from PyQt5.QtCore import QTimer

bandrate_dict = {1: '115200', 2: '921600', 3: '1500000', 4: '2000000'}


class UI_Func(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here"
    """
    def __init__(self, parent=None):
        super(UI_Func, self).__init__(parent)
        self.setupUi(self)
        self.bandrate.clear()
        self.port_check()
        self.ser = serial.Serial()

        for i, k in bandrate_dict.items():
            self.bandrate.addItem(k, i)
        self.Start_button.clicked.connect(self.selectionchange)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.data_receive)

        self.data_num_received = 0

    def selectionchange(self):
        portNum = self.port.currentText()
        baudrate = self.bandrate.currentText()
        self.serial_open_port(portNum, baudrate)
        print("click test")

    def port_check(self):
        self.Com_Dict = {}
        port_list = list(serial.tools.list_ports.comports())
        self.port.clear()
        for port in port_list:
            self.Com_Dict["%s" %port[0]] = "%s" %port[1]
            self.port.addItem(port[0])
        if len(self.Com_Dict) == 0:
            self.statusbar.showMessage("无串口")

    def serial_open_port(self, port, bandrate = 115200, bytesize = 8, stopbits = 1, parity = serial.PARITY_NONE):
        self.ser.port = port
        self.ser.baudrate = bandrate
        self.ser.stopbits = stopbits
        self.ser.parity = parity

        try:
            self.ser.open()
        except:
            self.statusbar.showMessage("串口打开失败")
            return None

        self.timer.start(2)
        if self.ser.is_open:
            self.statusbar.showMessage("串口已打开")


    def serial_close_port(self):
        self.timer.stop()
        try:
            self.ser.close()
        except:
            self.statusbar.showMessage("串口关闭失败")

    def data_receive(self):
        try:
            num = self.ser.inWaiting()
        except:
            self.serial_close_port()
            return None
        if num > 0:
            data = self.ser.readline(num)
            num = len(data)
            self.textBrowser.insertPlainText(data.decode('utf-8'))
            self.textBrowser.moveCursor(self.textBrowser.textCursor().End)
            self.data_num_received += num
            self.statusbar.showMessage("total data: %s" % str(self.data_num_received))

        else:
            pass





