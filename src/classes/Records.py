import os
import sqlite3

from PyQt5 import uic
from PyQt5.QtCore import QPropertyAnimation, QUrl
from PyQt5.QtGui import QFontDatabase, QFont, QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QMainWindow, QAction, QTableWidgetItem, QHeaderView, QAbstractItemView


class Records(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.initUI()
        self.path = __file__

    def initUI(self):
        uipath = os.path.join(os.path.dirname(__file__), "../ui/records.ui")
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
        self.textFont.setPixelSize(18)
        self.recordsFont = QFont(self.family)
        self.recordsFont.setPixelSize(15)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setFont(self.recordsFont)
        self.label_2.setFont(self.textFont)
        self.media_player = QMediaPlayer()
        self.clickURL = QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), "../sounds/click.mp3"))
        self.content = QMediaContent(self.clickURL)
        self.media_player.setMedia(self.content)
        self.bb = False
        self.getFromBase()

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

    def getFromBase(self):
        cur = self.con.cursor()
        res = cur.execute("""SELECT name, shootings, points 
        FROM records 
        ORDER BY shootings ASC, points DESC""").fetchall()
        self.table.setColumnCount(3)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem("Имя игрока"))
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem("Кол-во совершенных выстрелов"))
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem("Оставшиеся танки"))
        self.table.setRowCount(0)
        for i, row in enumerate(res):
            self.table.setRowCount(
                self.table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.table.setItem(
                    i, j, QTableWidgetItem(str(elem)))
