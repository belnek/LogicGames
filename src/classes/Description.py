import os
import sqlite3

from PyQt5 import uic
from PyQt5.QtCore import QPropertyAnimation, QUrl
from PyQt5.QtGui import QFontDatabase, QFont, QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QMainWindow, QAction, QTableWidgetItem, QHeaderView, QAbstractItemView


class Description(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.initUI()
        self.path = __file__

    def initUI(self):
        uipath = os.path.join(os.path.dirname(__file__), "../ui/description.ui")
        uic.loadUi(uipath, self)
        self.setFixedSize(800, 600)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "../ico.ico")))

        self.con = sqlite3.connect(os.path.join(os.path.dirname(__file__), "../bases/records.db"))

        showevent = QAction("Show", self)
        showevent.triggered.connect(self.showEvent)
        self.animation = QPropertyAnimation(self, b'windowOpacity')
        self.animation.setDuration(600)
        self.setWindowTitle("Танковая битва")
        self.finish = QAction("Quit", self)
        self.finish.triggered.connect(self.closeEvent)
        self.ttfId = QFontDatabase.addApplicationFont((os.path.join(os.path.dirname(__file__), "../ttf/minettf.ttf")))
        self.family = QFontDatabase.applicationFontFamilies(self.ttfId)[0]
        self.font().setFamily(self.family)
        self.textFont = QFont(self.family)
        self.textFont.setPixelSize(16)
        self.dFont = QFont(self.family)
        self.dFont.setPixelSize(15)
        self.label.setFont(self.textFont)
        self.text.setFont(self.dFont)
        self.media_player = QMediaPlayer()
        self.clickURL = QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), "../sounds/click.mp3"))
        self.content = QMediaContent(self.clickURL)
        self.media_player.setMedia(self.content)
        self.bb = False

    def doShow(self):
        print("a")
        self.show()
        try:
            if self.game.isEnabled():
                self.game.destroy()
        except Exception:
            pass
        try:
            self.animation.finished.disconnect(self.close)
        except:
            pass
        self.animation.stop()
        # Диапазон прозрачности постепенно увеличивается от 0 до 1.
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def doClose(self):
        self.bb = True
        self.animation.stop()
        self.animation.finished.connect(self.close)  # Закройте окно, когда анимация будет завершена
        # Диапазон прозрачности постепенно уменьшается с 1 до 0.
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

    def closeEvent(self, event):
        print("skgoghasjklghsdfg")
        if not self.bb:
            self.media_player.play()

            self.parent().showWin()
            self.doClose()
            event.ignore()
        else:
            event.accept()


