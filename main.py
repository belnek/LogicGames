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
from math import *

from Bullet import Bullet
from Tank import Tank


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.anim_group = None
        self.anim = QPropertyAnimation(None, b"pos")
        self.anim2 = QPropertyAnimation(None, b"pos")
        self.g = 9.8
        self.shootSpeed = 65
        self.currentTank = Tank()
        self.bullet = None
        self.initUI()

    def initUI(self):
        uipath = os.path.join(os.path.dirname(__file__), "ui.ui")
        uic.loadUi(uipath, self)
        app.setStyleSheet(PyQt5_stylesheets.load_stylesheet_pyqt5(style="style_navy"))

        self.setFixedSize(727, 886)

        # Отображаем содержимое QPixmap в объекте QLabel
        self.tank = Tank(self)
        self.tank.init(520, 680)
        self.tank.selectedNow.connect(lambda: self.tankchanged(self.tank))
        self.tank1 = Tank(self)
        self.tank1.init(320, 680)
        self.tank1.selectedNow.connect(lambda: self.tankchanged(self.tank1))
        # scaled_pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio

        self.verticalScroll.valueChanged.connect(self.on_value_vertical_changed)

        self.horizontalScroll.valueChanged.connect(self.on_value_horizontal_changed)
        self.shootButton.clicked.connect(lambda: self.makeShoot(self.currentTank))

        # self.makeShoot((self.tank.x, self.tank.y), self.target).connect(lambda: self.boom(self.target))

    def on_value_vertical_changed(self):
        value = self.verticalScroll.value()
        self.lcdVertical.display(value)

    def tankchanged(self, tank: Tank):
        if self.currentTank.isInit:
            self.currentTank.selected = not self.currentTank.selected
        self.currentTank = tank
    def on_value_horizontal_changed(self):
        value = self.horizontalScroll.value()
        self.lcdHorizontal.display(value)

    def boom(self, bullet):
        pass

    def makeShoot(self, start):
        if self.currentTank.isInit:
            self.bullet = Bullett(self)
            self.bullet.setStyleSheet("background-color:black;border-radius:5px;")
            self.bullet.resize(10, 10)
            self.bullet.move(int(start.x + 80 / 2), int(start.y + 50 / 2))
            self.bullet.show()
            tx, ty, t, h = self.solveTargetXY(start, self.shootSpeed, self.verticalScroll.value(),
                                              self.horizontalScroll.value())
            print(tx, ty)

            t = int(t * 1000 / 3)
            print(t)
            print(QPoint(int(tx + 80 / 2), int(ty + 50 / 2)))
            self.anim = QPropertyAnimation(self.bullet, b"pos")
            self.anim.setEndValue(
                QPoint(int(tx + 80 / 2), int(ty + 50 / 2)))
            self.anim.setDuration(t)
            self.anim.start()
            self.anim2 = QPropertyAnimation(self.bullet, b"size")
            self.anim2.setEndValue(QSize(int(10 + (h // 10)), int(10 + (h // 10))))
            self.anim2.setDuration(t // 2)
            self.anim3 = QPropertyAnimation(self.bullet, b"size")
            self.anim3.setEndValue(QSize(10, 10))
            self.anim3.setDuration(t // 2)
            self.anim_group = QParallelAnimationGroup()
            self.anim_group2 = QSequentialAnimationGroup()
            self.anim_group2.addAnimation(self.anim2)
            self.anim_group2.addAnimation(self.anim3)
            self.anim_group.addAnimation(self.anim)
            self.anim_group.addAnimation(self.anim_group2)
            self.anim_group.start()
            self.anim_group.finished.connect(lambda: self.boom(self.bullet))

    def solveTargetXY(self, start, speed, angleY, angleX):
        sx = start.x
        sy = start.y
        t = (2 * speed * sin(angleY * pi / 180)) / self.g
        r = speed * cos(angleY * pi / 180) * t
        maxx = r * cos((angleX - 90) * pi / 180)
        maxy = r * sin((angleX - 90) * pi / 180)

        tx = sx + maxx
        ty = sy + maxy
        h = (speed * speed * sin(angleY * pi / 180) * sin(angleY * pi / 180)) / (2 * self.g)

        return tx, ty, t, h


def excepthook(self, exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Oбнаружена ошибка !:", tb)


class Bullett(QWidget):

    def init(self, x, y):
        self.x = x
        self.y = y


if __name__ == '__main__':
    sys.excepthook = excepthook

    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
