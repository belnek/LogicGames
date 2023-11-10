import os

from PyQt5 import uic
from PyQt5.QtCore import QPropertyAnimation, QSize
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QDialog, QAction, QWidget, QMainWindow, QLabel
from PyQt5.uic.properties import QtGui


class LoadingDialog(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.initUI()

    def initUI(self):
        uipath = os.path.join(os.path.dirname(__file__), "../ui/loading.ui")
        uic.loadUi(uipath, self)
        self.setFixedSize(400, 300)
        showevent = QAction("Show", self)
        showevent.triggered.connect(self.showEvent)
        self.animation = QPropertyAnimation(self, b'windowOpacity')
        self.animation.setDuration(600)
        gif = QMovie(os.path.join(os.path.dirname(__file__), "loading.gif"))  # !!!
        gif.setScaledSize(QSize(70, 70))
        self.loading.setMovie(gif)
        self.l = QLabel(self)
        self.l.setMovie(gif)
        gif.start()
        gif.setParent(self)

        self.doShow()

    def doShow(self):
        print("a")

        self.animation.stop()
        # Диапазон прозрачности постепенно увеличивается от 0 до 1.
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def showWin(self):
        self.show()
        self.doShow()

    def doClose(self):
        self.animation.stop()
        # Диапазон прозрачности постепенно уменьшается с 1 до 0.
        self.animation.finished.connect(self.hide)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()
