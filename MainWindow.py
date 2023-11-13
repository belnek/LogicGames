import os
import sys
import threading
import traceback

from PyQt5 import uic
from PyQt5.QtCore import QPropertyAnimation, pyqtSignal, QUrl
from PyQt5.QtGui import QFontDatabase, QFont, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction

from src.classes.Description import Description
from src.classes.Instruction import Instruction
from src.classes.LoadingDialog import LoadingDialog
from src.classes.Records import Records
from src.classes.game import Game


class MainWin(QMainWindow):
    loading = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        self.path = __file__

    def initUI(self):
        uipath = os.path.join(os.path.dirname(__file__), "src/ui/main.ui")
        uic.loadUi(uipath, self)
        self.setFixedSize(727, 886)
        showevent = QAction("Show", self)
        showevent.triggered.connect(self.showEvent)
        self.setWindowTitle("Танковая битва")
        self.finish = QAction("Quit", self)
        self.finish.triggered.connect(self.closeEvent)
        self.ttfId = QFontDatabase.addApplicationFont("src/ttf/minettf.ttf")
        self.family = QFontDatabase.applicationFontFamilies(self.ttfId)[0]
        self.font().setFamily(self.family)
        self.labelf = QFont(self.family)
        self.labelf.setPixelSize(28)
        self.label.setFont(self.labelf)
        self.buttonsFont = QFont(self.family)
        self.buttonsFont.setPixelSize(18)
        for b in self.buttonsGroup.buttons():
            b.setFont(self.buttonsFont)
        self.startButton.clicked.connect(self.doCloseStart)
        self.recordsButton.clicked.connect(self.recordsButtonPressed)
        self.descriptionButton.clicked.connect(self.descriptionButtonPressed)
        self.instructionButton.clicked.connect(self.instructionButtonPressed)
        self.LogoPixmap = QPixmap(os.path.join(os.path.dirname(__file__), "src/images/logocompany2.png"))
        self.logo.setPixmap(self.LogoPixmap)
        self.animation = QPropertyAnimation(self, b'windowOpacity')
        self.animation.setDuration(600)
        self.bb = False
        self.media_player = QMediaPlayer()
        self.clickURL = QUrl.fromLocalFile("src/sounds/click.mp3")
        self.content = QMediaContent(self.clickURL)
        self.media_player.setMedia(self.content)
        self.doShow()

    def doShow(self):
        print("a")
        self.show()
        try:
            if self.game.isEnabled():
                self.game.destroy()
        except Exception:
            pass
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
        try:
            self.game.destroy()
        except Exception:
            pass

    def recordsButtonPressed(self):
        self.media_player.play()
        self.records = Records(self)
        self.records.doShow()
        self.doClose()
        self.records.show()

    def descriptionButtonPressed(self):
        self.media_player.play()
        self.description = Description(self)
        self.description.doShow()
        self.doClose()
        self.description.show()

    def instructionButtonPressed(self):
        self.media_player.play()
        self.instruction = Instruction(self)
        self.instruction.doShow()
        self.doClose()
        self.instruction.show()

    def doCloseStart(self):
        self.media_player.play()
        self.animation.stop()
        self.animation.finished.connect(self.start)  # Закройте окно, когда анимация будет завершена
        # Диапазон прозрачности постепенно уменьшается с 1 до 0.
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

    def doClose(self):

        self.animation.stop()
        # Диапазон прозрачности постепенно уменьшается с 1 до 0.
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

    def doCloseAll(self):

        self.animation.stop()

        self.animation.finished.connect(self.close)  # Закройте окно, когда анимация будет завершена
        # Диапазон прозрачности постепенно уменьшается с 1 до 0.
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

    def closeEvent(self, event):

        print("skgoghasjklghsdfg")
        if not self.bb:
            self.bb = True
            self.media_player.play()
            try:
                self.records.close()
            except Exception:
                pass

            try:
                self.instruction.close()
            except Exception:
                pass

            try:
                self.description.close()
            except Exception:
                pass

            try:
                self.game.close()
            except Exception:
                pass

            try:
                self.loadingDialog.close()
            except Exception:
                pass

            self.doCloseAll()
            event.ignore()
        else:
            self.hide()

            event.accept()

    def start(self):
        self.loadingDialog = LoadingDialog(parent=self)
        self.loadingDialog.show()

        # self.hide()
        self.loading.connect(self.loadingComplete)
        self.loadingStarted()
        # self.loadingDialog.doShow()

        # self.hide()

    def loadingStarted(self):
        self.game = Game(parent=self)
        self.game.loadingFinished.connect(self.loading.emit)
        self.game.initUI()

    def loadingComplete(self):
        print("asd")
        self.game.doShow()
        self.game.show()
        self.loadingDialog.doClose()
        print(self)


def excepthook(self, exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Oбнаружена ошибка !:", tb)


if __name__ == '__main__':
    sys.excepthook = excepthook

    app = QApplication(sys.argv)
    ex = MainWin()
    ex.show()
    sys.exit(app.exec())
