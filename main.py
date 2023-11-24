import sqlite3
import sys
import io

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidgetItem
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


class SearchWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("search.ui", self)
        # f = io.StringIO(template1)
        # uic.loadUi(f, self)
        self.info = []
        self.searchBtn.clicked.connect(self.search)
        self.listWidget.itemClicked.connect(self.show_book)

    def search(self):
        search_text = self.lineEdit.text()
        con = sqlite3.connect("books.sqlite")
        cur = con.cursor()
        if self.comboBox.currentText() == 'Название':
            res = cur.execute(f"""
            SELECT * FROM books
            WHERE title LIKE '%{search_text}%'
            """).fetchall()
        else:
            res = cur.execute(f"""
            SELECT * FROM books
            WHERE author LIKE '%{search_text}%'
            """).fetchall()

        self.info = []
        self.listWidget.clear()
        for elem in res:
            item = QListWidgetItem(elem[2])
            item.setTextAlignment(Qt.AlignHCenter)
            self.listWidget.addItem(item)
            self.info.append(elem)

    def show_book(self):
        i = self.listWidget.currentRow()
        print(i)
        print(self.info[i])
        self.book = BookWidget(self.info[i])
        self.book.show()


class BookWidget(QMainWindow):
    def __init__(self, info):
        super().__init__()
        uic.loadUi("book.ui", self)
        # f = io.StringIO(template1)
        # uic.loadUi(f, self)
        if info[1]:
            self.pixmap = QPixmap.fromImage(QImage(info[1]))
        else:
            self.pixmap = QPixmap.fromImage(QImage('default.jpg'))
        self.lbl.setPixmap(self.pixmap)
        self.lbl.setScaledContents(True);

        self.title.setText(info[2])
        self.author.setText(info[3])
        self.year.setText(str(info[4]))
        self.genre.setText(info[5])

        self.title = info


def except_hook(cls, exception, traceback):
    sys.excepthook(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SearchWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
