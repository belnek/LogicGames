import os
import sys
import time
import traceback
from threading import Timer
from os.path import abspath
import PyQt5_stylesheets
from PyQt5 import uic, QtCore
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QPoint, QParallelAnimationGroup, QTimer, QRect, QSize, \
    QSequentialAnimationGroup, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMainWindow
from PyQt5.uic import pyuic

from LogicGames.Tank import Tank


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.anim_group = None
        self.anim = QPropertyAnimation(None, b"pos")
        self.anim2 = QPropertyAnimation(None, b"pos")
        self.child = None
        self.initUI()

    def initUI(self):
        uipath = os.path.join(os.path.dirname(__file__), "ui.ui")
        uic.loadUi(uipath, self)
        app.setStyleSheet(PyQt5_stylesheets.load_stylesheet_pyqt5(style="style_navy"))

        self.setFixedSize(727, 886)

        # Отображаем содержимое QPixmap в объекте QLabel
        self.tank = Tank(self)
        self.tank.init(10, 10)
        self.tank.rotate_180()


        # scaled_pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio
        self.target = QWidget(self)
        self.target.setStyleSheet("background-color:red;border-radius:5px;")
        self.target.resize(40, 40)
        self.target.move(10, 330)
        self.verticalScroll.valueChanged.connect(self.on_value_vertical_changed)
        self.horizontalScroll.valueChanged.connect(self.on_value_horizontal_changed)

        self.makeShoot(self.tank, self.target).connect(lambda: self.boom(self.target))
        #self.makeShoot((self.tank.x, self.tank.y), self.target).connect(lambda: self.boom(self.target))

    def on_value_vertical_changed(self):
        value = self.verticalScroll.value()
        self.lcdVertical.display(value)

    def on_value_horizontal_changed(self):
        value = self.horizontalScroll.value()
        self.lcdHorizontal.display(value)

    def boom(self, target):
        target.setStyleSheet("background-color:black;border-radius:5px;")

    def aiming(self):
        QtCore.QTimer.set

    def makeShoot(self, start, target):
        self.child = QWidget(self)
        self.child.setStyleSheet("background-color:black;border-radius:5px;")
        self.child.resize(10, 10)
        self.child.move(int(start.x + start.rect().width() / 2), int(start.y + start.rect().height() / 2))
        self.anim = QPropertyAnimation(self.child, b"pos")
        self.anim.setEndValue(
            QPoint(int(target.x() + target.rect().width() / 2), int(target.y() + target.rect().height() / 2)))
        self.anim.setDuration(3300)
        self.anim2 = QPropertyAnimation(self.child, b"size")
        self.anim2.setEndValue(QSize(20, 20))
        self.anim2.setDuration(1650)
        self.anim3 = QPropertyAnimation(self.child, b"size")
        self.anim3.setEndValue(QSize(10, 10))
        self.anim3.setDuration(1650)
        self.anim_group = QParallelAnimationGroup()
        self.anim_group2 = QSequentialAnimationGroup()
        self.anim_group2.addAnimation(self.anim2)
        self.anim_group2.addAnimation(self.anim3)
        self.anim_group.addAnimation(self.anim)
        self.anim_group.addAnimation(self.anim_group2)
        self.anim_group.start()
        return self.anim_group.finished


def excepthook(self, exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Oбнаружена ошибка !:", tb)


if __name__ == '__main__':
    sys.excepthook = excepthook

    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
