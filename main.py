import sqlite3
import sys

from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QTableWidgetItem
from pyqt5_plugins.examplebutton import QtWidgets
from Ui import addEditCoffeeForm
from Ui import main_design

data = {}
genreText = ''


class PreDialog(QDialog, addEditCoffeeForm.Ui_Dialog):
    def __init__(self, parent=None, name=" ", st=" ", type_=" ", op=" ", check=" ", V=" "):
        global data
        super(PreDialog, self).__init__(parent)
        self.parent = parent

        self.setupUi(self)
        self.setWindowTitle('Добавить элемент')
        self.lineEdit_2.setText(name)
        self.lineEdit.setText(st)
        self.lineEdit_3.setText(type_)
        self.lineEdit_4.setText(op)
        self.lineEdit_5.setText(check)
        self.lineEdit_6.setText(V)

        data = None

        self.pushButton.clicked.connect(self.onClick)

    def onClick(self):
        global data
        data = {'название сорта': self.lineEdit_2.text(),
                'степень обжарки': self.lineEdit.text(),
                'молотый/в зернах': self.lineEdit_3.text(),
                'описание вкуса': self.lineEdit_4.text(),
                'цена': self.lineEdit_5.text(),
                'объем упаковки': self.lineEdit_6.text()}
        self.accept()

    def closeEvent(self, event):
        self.parent.show()


class Example(QMainWindow, main_int.Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.result = []
        self.maxID = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Фильмотека')
        self.update_()
        self.pushButton.clicked.connect(self.addFilm)
        self.pushButton_2.clicked.connect(self.updateFilm)

    def update_(self):
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена', 'объем упаковки'])
        self.tableWidget.setRowCount(0)
        con = sqlite3.connect("data/coffee.sqlite")
        cur = con.cursor()
        res = list(cur.execute("""SELECT * FROM COFFEE"""))
        for i in range(len(res)):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j in range(len(res[i])):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(res[i][j])))

        con.close()

    def addFilm(self):
        dialog = PreDialog(self)
        result = dialog.exec_()
        if result == QtWidgets.QDialog.Accepted:
            self.maxID += 1
            con = sqlite3.connect("data/coffee.sqlite")
            cur = con.cursor()
            cur.execute(f"""INSERT INTO COFFEE VALUES 
            ({self.maxID}, '{data['название сорта']}', '{data['степень обжарки']}', 
            '{data['молотый/в зернах']}', '{data['описание вкуса']}', '{data['цена']}', '{data['объем упаковки']}')""")
            con.commit()
            con.close()
            self.update_()

    def updateFilm(self):
        idx = self.tableWidget.currentIndex().row()
        a = self.tableWidget.item(idx, 3).text()

        dialog = PreDialog(self, name=self.tableWidget.item(idx, 1).text(),
                           st=self.tableWidget.item(idx, 2).text(),
                           type_=self.tableWidget.item(idx, 3).text(),
                           op=self.tableWidget.item(idx, 4).text(),
                           check=self.tableWidget.item(idx, 5).text(),
                           V=self.tableWidget.item(idx, 6).text())
        result = dialog.exec_()
        if result == QtWidgets.QDialog.Accepted:
            con = sqlite3.connect("data/coffee.sqlite")
            cur = con.cursor()
            cur.execute(f"""UPDATE COFFEE
                            SET 'название сорта'='{data['название сорта']}', 
                            'степень обжарки' = '{data['степень обжарки']}', 
                            'молотый/в зернах' = '{data['молотый/в зернах']}', 
                            'описание вкуса'='{data['описание вкуса']}',
                            'цена'='{data['цена']}',
                            'объем упаковки'='{data['объем упаковки']}'
                            WHERE id={self.tableWidget.item(idx, 0).text()}""")
            con.commit()
            self.update_()

            con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
