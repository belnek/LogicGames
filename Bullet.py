from PyQt5.QtWidgets import QGraphicsRectItem, QWidget


class Bullet(QWidget):

    def init(self, x, y):
        self.x = x
        self.y = y

