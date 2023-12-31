import os

from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from PyQt5.QtGui import QImage, QPixmap, QTransform
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QLabel


class Tank(QLabel):
    clicked = pyqtSignal()
    selectedNow = pyqtSignal()
    isInit = False

    def init(self, x, y, idd):
        self.isShooting = False
        self.player = True
        self.x = x
        self.y = y
        self.sizeX = 43
        self.sizeY = 36
        self.resize(self.sizeX + 10, self.sizeY + 10)
        self.pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "../images/tank.png")).scaled(self.sizeX, self.sizeY)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.setPixmap(self.pixmap)
        self.move(self.x, self.y)
        self._selected = False
        self.angleX = 0
        self.angleY = 0
        self.isAlive = True
        self.shootsEstimated = 3
        self.isInit = True
        self.id = idd
        self.media_player = QMediaPlayer()
        self.clickURL = QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), "../sounds/tankClick.mp3"))
        self.content = QMediaContent(self.clickURL)
        self.media_player.setMedia(self.content)
        self.clicked.connect(lambda: self.tankClicked())

    def setting(self, x, y, idd):
        self.player = True
        self.x = x
        self.y = y
        self.resize(self.sizeX + 10, self.sizeY + 10)
        self.pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "../images/tank.png")).scaled(self.sizeX, self.sizeY)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.setPixmap(self.pixmap)
        self.move(self.x, self.y)
        self._selected = False
        self.angleX = 0
        self.angleY = 0
        self.isAlive = True
        self.shootsEstimated = 3
        self.isInit = True
        self.id = idd

    def setImg(self):
        self.pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "../images/tank.png")).scaled(self.sizeX, self.sizeY)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.setPixmap(self.pixmap)

    def tankClicked(self):
        print("asd")
        print(self.isShooting)
        if not self.isShooting and self.shootsEstimated > 0:
            self.media_player.stop()
            self.media_player.play()
            self.selected = not self._selected
            self.selectedNow.emit()

    def rotate_180(self):
        image = QImage(os.path.join(os.path.dirname(__file__), "../images/tank.png")).scaled(self.sizeX, self.sizeY)
        self.angleX = 180
        rotated_image = image.transformed(QTransform().rotate(self.angleX))
        pixmap = QPixmap.fromImage(rotated_image)

        self.setPixmap(pixmap)
        self.player = not self.player

    def rotate(self, angle):
        image = QImage(os.path.join(os.path.dirname(__file__), "../images/tank.png")).scaled(self.sizeX, self.sizeY)
        rotated_image = image.transformed(QTransform().rotate(self.angleX + angle))

        pixmap = QPixmap.fromImage(rotated_image)

        self.setPixmap(pixmap)

    def mousePressEvent(self, ev):
        print("click")
        if self.isAlive and self.player:
            self.clicked.emit()

    def shooted(self):
        self.isAlive = False
        self.pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "../images/tankShooted.png")).scaled(self.sizeX, self.sizeY)\
            .transformed(QTransform().rotate(self.angleX))
        # Отображаем содержимое QPixmap в объекте QLabel
        self.setPixmap(self.pixmap)

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, nselected):
        self._selected = nselected
        if nselected:
            self.pixmap = QPixmap(os.path.join(os.path.dirname(__file__),
                                               "../images/tankSelected.png")).scaled(self.sizeX,
                                                                                     self.sizeY).transformed(
                QTransform().rotate(self.angleX))
            # Отображаем содержимое QPixmap в объекте QLabel
            self.setPixmap(self.pixmap)
        else:

            self.pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "../images/tank.png")).scaled(self.sizeX,
                                                                                                        self.sizeY).transformed(
                QTransform().rotate(self.angleX))
            # Отображаем содержимое QPixmap в объекте QLabel
            self.setPixmap(self.pixmap)
