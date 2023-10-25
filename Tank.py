import os

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QTransform
from PyQt5.QtWidgets import QLabel


class Tank(QLabel):
    clicked = pyqtSignal()
    selectedNow = pyqtSignal()
    isInit = False

    def init(self, x, y):

        self.player = True
        self.x = x
        self.y = y
        self.resize(80, 50)
        self.pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "tank.png")).scaled(80, 50)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.setPixmap(self.pixmap)
        self.move(self.x, self.y)
        self._selected = False
        self.angleX = 0
        self.angleY = 0
        self.isAlive = True
        self.shootsEstimated = 3
        self.isInit = True

        self.clicked.connect(lambda: self.tankClicked())

    def tankClicked(self):
        self.selected = not self._selected
        self.selectedNow.emit()

    def rotate_180(self):
        image = QImage(os.path.join(os.path.dirname(__file__), "tank.png")).scaled(80, 50)

        rotated_image = image.transformed(QTransform().rotate(180 + self.angleX))

        pixmap = QPixmap.fromImage(rotated_image)

        self.setPixmap(pixmap)
        self.player = not self.player

    def rotate(self, angle):
        image = QImage(os.path.join(os.path.dirname(__file__), "tank.png")).scaled(80, 50)

        rotated_image = image.transformed(QTransform().rotate(self.angleX + angle))

        pixmap = QPixmap.fromImage(rotated_image)

        self.setPixmap(pixmap)
    def mousePressEvent(self, ev):
        if self.isAlive:
            self.clicked.emit()

    def shooted(self):
        self.isAlive = False
        self.pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "tankShooted.png")).scaled(80, 50).transformed(QTransform().rotate(self.angleX))
        # Отображаем содержимое QPixmap в объекте QLabel
        self.setPixmap(self.pixmap)

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, nselected):
        self._selected = nselected
        if nselected:
            print(1)
            self.pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "tankSelected.png")).scaled(80, 50).transformed(QTransform().rotate(self.angleX))
            # Отображаем содержимое QPixmap в объекте QLabel
            self.setPixmap(self.pixmap)
        else:
            print(0)

            self.pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "tank.png")).scaled(80, 50).transformed(QTransform().rotate(self.angleX))
            # Отображаем содержимое QPixmap в объекте QLabel
            self.setPixmap(self.pixmap)
