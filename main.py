import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

data = {}


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.result = []
        self.maxID = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Фильмотека')
        self.update_()

    def update_(self):
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена', 'объем упаковки'])
        self.tableWidget.setRowCount(0)
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        res = list(cur.execute("""SELECT * FROM COFFEE"""))
        for p in range(len(res)):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for q in range(len(res[p])):
                self.tableWidget.setItem(p, q, QTableWidgetItem(str(res[p][q])))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
