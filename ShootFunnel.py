import os

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QTransform
from PyQt5.QtWidgets import QLabel


class ShootFunnel(QLabel):
    clicked = pyqtSignal()
    selectedNow = pyqtSignal()
    isInit = False

    def init(self, x, y):

        self.x = x
        self.y = y
        self.resize(30, 30)
        self.pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "ShootFunnel.png")).scaled(30, 30)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.setPixmap(self.pixmap)
        self.move(self.x, self.y)
        self.isInit = True



