import os
import random
import sys
import time
import traceback
from threading import Timer
from os.path import abspath
import PyQt5_stylesheets
from PyQt5 import uic, QtCore
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QPoint, QParallelAnimationGroup, QTimer, QRect, QSize, \
    QSequentialAnimationGroup, Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor, QPen
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMainWindow
from PyQt5.uic import pyuic
from math import *

from ShootFunnel import ShootFunnel
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
        self.mainWin = self
        self.playerTanks = list()
        self.AITanks = list()
        self.initUI()
        self.isPlayerTurn = True

    def initUI(self):
        uipath = os.path.join(os.path.dirname(__file__), "ui.ui")
        uic.loadUi(uipath, self)

        # self.setFixedSize(727, 886)
        self.playerTanks = [Tank(self) for i in range(30)]
        self.AITanks = [Tank(self) for i in range(30)]
        c = 0
        for i in self.playerTanks:
            i.init(300, 300, c)

            c += 1

        for i in self.AITanks:
            i.init(300, 300, c)
            c += 1
        # Отображаем содержимое QPixmap в объекте QLabel

        '''
        self.tank1 = Tank(self)
        self.tank1.init(320, 680)
        self.tank1.selectedNow.connect(lambda: self.tankchanged(self.tank1))
        
        
        self.playerTanks = {self.tank, self.tank1}'''

        self.setPlayersTanks()
        self.setAITanks()
        # scaled_pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio

        self.verticalScroll.valueChanged.connect(self.on_value_vertical_changed)

        self.horizontalScroll.valueChanged.connect(self.on_value_horizontal_changed)

        self.shootButton.clicked.connect(lambda: self.makeShoot(self.currentTank))

        # self.makeShoot((self.tank.x, self.tank.y), self.target).connect(lambda: self.boom(self.target))

    def on_value_vertical_changed(self):
        value = self.verticalScroll.value()
        self.lcdVertical.display(value)

    def on_value_horizontal_changed(self):
        value = self.horizontalScroll.value()
        self.lcdHorizontal.display(value)

    def setPlayersTanks(self):

        width = self.playerTanks[0].width()
        height = self.playerTanks[0].height()
        segmentsx = int(660 / width)
        segmentsy = int((670 - 390) / height)
        listOfPotencialSegments = list()
        for i in range(segmentsx):
            random.seed(random.randint(0, 10000000))

            for j in range(segmentsy):
                ii = random.randint(0, 2)

                jj = random.randint(0, 1)
                while i + ii > segmentsx:
                    ii = random.randint(0, 2)

                i += ii

                while j + jj > segmentsx:
                    jj = random.randint(0, 1)

                j += jj
                listOfPotencialSegments.append((i, j))
        n = len(self.playerTanks)
        random.seed(random.randint(0, 10000000))

        segments = random.sample(listOfPotencialSegments, n)

        newSegments = list(tuple())
        for i in segments:
            xx = i[0] * width
            yy = i[1] * height + 390
            newSegments.append((xx, yy))
        c = 0
        for tank in self.playerTanks:
            tank.setting(*newSegments[c], tank.id)
            c += 1
            tank.selectedNow.connect(lambda: self.tankchanged())
        self.setAITanks()

    def setAITanks(self):
        print("s")
        print("asfasf")

        width = self.AITanks[0].width()
        height = self.AITanks[0].height()
        segmentsx = int(500 / width)
        segmentsy = int((360) / height)
        listOfPotencialSegments = list()
        print("s")
        for i in range(segmentsx):
            random.seed(random.randint(0, 10000000))

            for j in range(segmentsy):
                ii = random.randint(0, 2)

                jj = random.randint(0, 1)
                while i + ii > segmentsx:
                    ii = random.randint(0, 2)

                i += ii

                while j + jj > segmentsx:
                    jj = random.randint(0, 1)

                j += jj
                listOfPotencialSegments.append((i, j))
        n = len(self.AITanks)
        random.seed(random.randint(0, 10000000))

        segments = random.sample(listOfPotencialSegments, n)
        print(segments)

        newSegments = list(tuple())
        for i in segments:
            xx = i[0] * width
            yy = i[1] * height
            newSegments.append((xx, yy))
        c = 0
        for tank in self.AITanks:
            tank.setting(*newSegments[c], tank.id)
            tank.rotate_180()
            c += 1

    def tankchanged(self):
        tank = self.sender()

        if self.currentTank.isInit:
            self.currentTank.selected = not self.currentTank.selected
        self.currentTank = tank
        print(self.currentTank.x, self.currentTank.y)
        self.horizontalScroll.setValue(int(self.currentTank.angleX))
        self.lcdHorizontal.display(self.currentTank.angleX)
        self.verticalScroll.setValue(int(self.currentTank.angleY))
        self.lcdVertical.display(self.currentTank.angleY)

    def checkHit(self, pos):
        shootedTank = Tank(self)
        ul = pos.geometry().topLeft()
        br = pos.geometry().bottomRight()
        isTank = False
        for tank in self.AITanks:
            ult = tank.geometry().topLeft()
            brt = tank.geometry().bottomRight()
            if ult.x() <= ul.x() <= brt.x() and ult.y() <= ul.y() <= brt.y() and ult.x() <= br.x() <= brt.x() and ult.y() <= br.y() <= brt.y():
                isTank = True
                shootedTank = tank
        if not self.isPlayerTurn:
            isTank = False
            shootedTank = Tank()
        for tank in self.playerTanks:
            ult = tank.geometry().topLeft()
            brt = tank.geometry().bottomRight()
            if ult.x() <= ul.x() <= brt.x() and ult.y() <= ul.y() <= brt.y() and ult.x() <= br.x() <= brt.x() and ult.y() <= br.y() <= brt.y():
                isTank = True
                shootedTank = tank

        return isTank, shootedTank

    def boom(self, bullet: QWidget):
        isTank, shootedTank = self.checkHit(bullet)
        if isTank:

            shootedTank.shooted()
            if shootedTank.player:
                self.playerTanks.remove(shootedTank)
            else:
                self.AITanks.remove(shootedTank)
            self.layout().removeWidget(bullet)
            print(len(self.playerTanks), len(self.AITanks))
            bullet.deleteLater()

            bullet.destroy(True)
        else:
            funnel = ShootFunnel(self)
            funnel.init(bullet.x() - int(bullet.width()), bullet.y())
            self.layout().addWidget(funnel)
            funnel.show()
            self.layout().removeWidget(bullet)
            bullet.deleteLater()

            bullet.destroy(True)
        for tank in self.playerTanks:
            tank.isShooting = False
        self.currentTank.selected = False
        if self.currentTank == shootedTank:
            self.currentTank.shooted()

        self.currentTank = Tank()
        self.widget.show()
        self.horizontalScroll.setValue(0)
        self.lcdHorizontal.display(0)
        self.verticalScroll.setValue(0)
        self.lcdVertical.display(0)
        shootings = 0
        playerTanks = 0
        if self.isPlayerTurn:
            self.widget.hide()
            for tank in self.playerTanks:
                shootings += tank.shootsEstimated
            if shootings == 0 and len(self.AITanks) > 0:

                if len(self.playerTanks) > 0:
                    print(f"Игра окончена! У вас осталось {len(self.playerTanks)} танков и не осталось снярядов. У соперника осталось {len(self.AITanks)}")
                else:
                    print(f"Игра окончена! У вас не осталось танков. У соперника осталось {len(self.AITanks)}")
            if len(self.AITanks) == 0:
                print(f"Вы победили! Вы уничтожили все танки соперника. У вас осталось {len(self.playerTanks)}")
            shootings = 0
            for tank in self.AITanks:
                shootings += tank.shootsEstimated
            if shootings == 0:
                print(f"Вы победили! Соперник сдался, так как у него закончились снаряды. У вас осталось {len(self.playerTanks)}")
            self.isPlayerTurn = False

            self.AITurn()
        else:
            for tank in self.AITanks:
                shootings += tank.shootsEstimated

            self.isPlayerTurn = True

    def tick(self, start, angleX):

        if self.currentTank.angleX != angleX:
            if angleX > self.currentTank.angleX:
                self.currentTank.rotate(1)
                self.currentTank.angleX += 1
                QTimer.singleShot(50, lambda: self.tick(start, angleX))
            elif angleX < self.currentTank.angleX:
                self.currentTank.rotate(-1)
                self.currentTank.angleX -= 1
                QTimer.singleShot(50, lambda: self.tick(start, angleX))
            else:
                if self.currentTank.angleX > 0:
                    self.currentTank.rotate(-1)
                    self.currentTank.angleX -= 1
                    QTimer.singleShot(50, lambda: self.tick(start, angleX))
                else:
                    self.currentTank.rotate(1)
                    self.currentTank.angleX += 1
                    QTimer.singleShot(50, lambda: self.tick(start, angleX))
            print(self.currentTank.angleX, angleX)

        else:
            self.currentTank.shootsEstimated -= 1
            self.bullet = QWidget(self)
            self.bullet.setStyleSheet("background-color:black;border-radius:5px;")
            self.bullet.resize(10, 10)

            self.bullet.move(int(start.x + start.width() / 3),
                             int(start.y + start.height() / 2))
            self.bullet.show()

            tx, ty, t, h = self.solveTargetXY(start, self.shootSpeed, self.currentTank.angleY,
                                              self.currentTank.angleX)
            t = int(t * 1000 / 3)
            self.anim = QPropertyAnimation(self.bullet, b"pos")
            self.anim.setEndValue(
                QPoint(int(tx + start.width() / 3), int(ty + start.height() / 2)))
            self.anim.setDuration(t)
            self.anim.finished.connect(lambda: self.boom(self.bullet))
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

    def AITurn(self):
        currentAITank = random.choice(self.AITanks)
        sh = currentAITank.shootsEstimated
        while sh == 0:
            currentAITank = random.choice(self.AITanks)
            sh = currentAITank.shootsEstimated
        isHitNum = random.randint(0, 100)
        print(isHitNum)
        if isHitNum >= 20:
            recurs = 0
            angleX = random.randint(-90, 90)
            angleY = random.randint(0, 90)
            self.currentTank = currentAITank
            self.currentTank.angleY = angleY
            bull = QWidget()
            bull.resize(10, 10)

            bull.move(int(self.currentTank.x + self.currentTank.width() / 3),
                      int(self.currentTank.y + self.currentTank.height() / 2))
            x, y, _, __ = self.solveTargetXY(bull, self.shootSpeed, angleY, angleX)
            bull.move(int(x), int(y))
            res, _ = self.checkHit(bull)
            print(res)
            while not res:
                recurs += 1
                angleX = 180 + random.randint(-90, 90)
                angleY = random.randint(0, 90)
                self.currentTank = currentAITank
                self.currentTank.angleY = angleY
                bull = QWidget()
                bull.resize(10, 10)

                bull.move(int(self.currentTank.x + self.currentTank.width() / 3),
                          int(self.currentTank.y + self.currentTank.height() / 2))
                x, y, _, __ = self.solveTargetXY(bull, self.shootSpeed, angleY, angleX)
                bull.move(int(x), int(y))
                res, _ = self.checkHit(bull)
                if recurs > 2000:
                    self.AITurn()
                    return
                print(res)

            QTimer.singleShot(50, lambda: self.tick(self.currentTank, angleX))

        else:
            angleX = 180 + random.randint(-90, 90)
            angleY = random.randint(0, 90)
            self.currentTank = currentAITank
            self.currentTank.angleY = angleY
            bull = QWidget()
            bull.resize(10, 10)
            bull.move(int(self.currentTank.x + self.currentTank.width() / 3),
                      int(self.currentTank.y + self.currentTank.height() / 2))
            x, y, _, __ = self.solveTargetXY(bull, self.shootSpeed, angleY, angleX)
            bull.move(int(x), int(y))
            res, _ = self.checkHit(bull)
            while res:
                angleX = random.randint(-90, 90)
                angleY = random.randint(0, 90)
                self.currentTank = currentAITank
                self.currentTank.angleY = angleY
                bull = QWidget()
                bull.resize(10, 10)
                bull.move(int(self.currentTank.x + self.currentTank.width() / 3),
                          int(self.currentTank.y + self.currentTank.height() / 2))
                x, y, _, __ = self.solveTargetXY(bull, self.shootSpeed, angleY, angleX)
                bull.move(int(x), int(y))
                res, _ = self.checkHit(bull)
                print(res)

            QTimer.singleShot(50, lambda: self.tick(self.currentTank, angleX))

    def makeShoot(self, start):

        if self.currentTank.isInit:

            if self.currentTank.shootsEstimated > 0 and self.verticalScroll.value() != 0:
                for t in self.playerTanks:
                    t.isShooting = True
                self.currentTank.angleY = self.verticalScroll.value()
                self.widget.hide()
                QTimer.singleShot(50, lambda: self.tick(start, self.horizontalScroll.value()))

    def solveTargetXY(self, start, speed, angleY, angleX):
        sx = start.x
        sy = start.y
        if type(sx) != float and type(sx) != int:
            sx = start.x()
            sy = start.y()
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


if __name__ == '__main__':
    sys.excepthook = excepthook

    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
