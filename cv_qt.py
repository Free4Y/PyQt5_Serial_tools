import sys
import cv2
import numpy as np

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Video():
    def __init__(self, capture):
        self.capture = capture
        self.currentFrame = np.array([])

    # def captureFrame(self):
    #     ret, readFrame = self.capture.read()
    #     return readFrame

    def captureNextFrame(self):
        ret, readFrame = self.capture.read()
        if (ret == True):
            self.currentFrame = cv2.cvtColor(readFrame, cv2.COLOR_BGR2RGB)

    def convertFrame(self):
        try:
            height, width = self.currentFrame.shape[:2]
            image = QImage(self.currentFrame, width, height, QImage.Format_RGB888)
            img = QPixmap.fromImage(image)
            self.previousFrame = self.currentFrame
            return img
        except:
            return None


class Gui(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(250, 80, 800, 600)
        self.setWindowTitle('Test')
        self.video = Video(cv2.VideoCapture(0, cv2.CAP_DSHOW))
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.play)
        self._timer.start(27)
        self.update()
        self.videoFrame = QLabel('VideoCapture')
        self.videoFrame.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.videoFrame)

        self.ret, self.capturedFrame = self.video.capture.read()

    def play(self):
        try:
            self.video.captureNextFrame()
            self.videoFrame.setPixmap(self.video.convertFrame())
            self.videoFrame.setScaledContents(True)
        except TypeError:
            print('No frame')

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes|QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.video.capture.release()
            print('release cap')
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Gui()
    ex.show()
    sys.exit(app.exec_())

