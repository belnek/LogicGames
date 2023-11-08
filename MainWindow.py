import os
import sys
import traceback

from PyQt5 import uic
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtGui import QFontDatabase, QFont, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QButtonGroup, QAction

from game import Game


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uipath = os.path.join(os.path.dirname(__file__), "main.ui")
        uic.loadUi(uipath, self)
        self.setFixedSize(727, 886)
        showevent = QAction("Show", self)
        showevent.triggered.connect(self.showEvent)

        finish = QAction("Quit", self)
        finish.triggered.connect(self.closeEvent)
        self.ttfId = QFontDatabase.addApplicationFont("minettf.ttf")
        self.family = QFontDatabase.applicationFontFamilies(self.ttfId)[0]
        self.font().setFamily(self.family)
        self.labelf = QFont(self.family)
        self.labelf.setPixelSize(25)
        self.label.setFont(self.labelf)
        self.buttonsFont = QFont(self.family)
        self.buttonsFont.setPixelSize(15)
        for b in self.buttonsGroup.buttons():
            b.setFont(self.buttonsFont)
        self.startButton.clicked.connect(self.doClose)
        self.LogoPixmap = QPixmap(os.path.join(os.path.dirname(__file__), "logocompany2.png"))
        self.logo.setPixmap(self.LogoPixmap)
        self.animation = QPropertyAnimation(self, b'windowOpacity')
        self.animation.setDuration(600)
        self.doShow()

    def doShow(self):
        print("a")
        try:
            self.animation.finished.disconnect(self.start)
        except:
            pass
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
        self.animation.finished.connect(self.start)  # Закройте окно, когда анимация будет завершена
        # Диапазон прозрачности постепенно уменьшается с 1 до 0.
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

    def doCloseAll(self):
        self.animation.stop()
        self.animation.finished.connect(sys.exit)  # Закройте окно, когда анимация будет завершена
        # Диапазон прозрачности постепенно уменьшается с 1 до 0.
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

    def closeEvent(self, event):
        print("skgoghasjklghsdfg")
        self.doCloseAll()
        event.ignore()

    def start(self):
        self.game = Game(self)

        # self.hide()
        self.game.show()


def excepthook(self, exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Oбнаружена ошибка !:", tb)


if __name__ == '__main__':
    sys.excepthook = excepthook

    app = QApplication(sys.argv)
    ex = MainWin()
    ex.show()
    sys.exit(app.exec())
