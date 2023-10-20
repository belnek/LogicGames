import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QTransform
from PyQt5.QtWidgets import QLabel


class Tank(QLabel):
    def init(self, x, y):
        self.player = True
        self.x = x
        self.y = y
        self.resize(80, 50)
        self.pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "tank.png")).scaled(80, 50)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.setPixmap(self.pixmap)
        self.move(self.x, self.y)





    def rotate_180(self):
        image = QImage(os.path.join(os.path.dirname(__file__), "tank.png")).scaled(80, 50)

        rotated_image = image.transformed(QTransform().rotate(180))

        pixmap = QPixmap.fromImage(rotated_image)

        self.setPixmap(pixmap)
        self.player = False
