import sys
import sqlite3
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QDialogButtonBox, QSpinBox
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel
from UI.addEditCoffeeForm import Ui_Dialog
from UI.main import Ui_MainWindow

con = sqlite3.connect('data/coffee.sqlite')
cur = con.cursor()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('data/coffee.sqlite')
        self.db.open()
        self.model = QSqlQueryModel(self)
        self.request = '''SELECT Coffee.ID, Sorts.name as "Сорт", Roasting.title as 
        "Степень прожарки", Ground_in_grains.title as "Молотый/в зернах", taste_description as
        "Описание вкуса", price as "Цена", volume as "Объём пачки" FROM Coffee
        INNER JOIN Sorts ON Sorts.ID = Coffee.sort
        INNER JOIN Roasting ON Roasting.ID = Coffee.roasting
        INNER JOIN Ground_in_grains ON Ground_in_grains.ID = Coffee.ground_in_grains'''
        self.model.setQuery(self.request)
        self.tableView.setModel(self.model)
        self.tableView.resizeColumnsToContents()
        self.add.clicked.connect(self.add_coffee)
        self.reload_btn.clicked.connect(self.reload)

    def reload(self):
        self.model.setQuery(self.request)
        self.tableView.setModel(self.model)
        self.tableView.resizeColumnsToContents()

    def add_coffee(self):
        self.d = Dialog()
        self.d.show()


class Dialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.add)

    def add(self):
        sort = cur.execute(f'''SELECT ID FROM Sorts
        WHERE name = "{self.sort.text()}"''').fetchone()
        roasting = cur.execute(f'''SELECT ID FROM Roasting
        WHERE title = "{self.obj.text()}"''').fetchone()
        if self.ground.isChecked():
            ground_in_grains = 2
        else:
            ground_in_grains = 1
        if not sort:
            cur.execute(f'''INSERT INTO Sorts(name) VALUES("{self.sort.text()}")''')
            con.commit()
            sort = cur.execute(f'''SELECT ID FROM Sorts
            WHERE name = "{self.sort.text()}"''').fetchone()
        if not roasting:
            cur.execute(f'''INSERT INTO Roasting(title) VALUES("{self.obj.text()}")''')
            con.commit()
            roasting = cur.execute(f'''SELECT ID FROM Roasting
            WHERE title = "{self.obj.text()}"''').fetchone()
        print(sort[0], roasting[0], ground_in_grains, self.deskr.text(), self.price.value(),
              self.volume.value())
        cur.execute(f'''INSERT INTO Coffee(sort, roasting, ground_in_grains, taste_description,
         price, volume) VALUES({sort[0]}, {roasting[0]}, {ground_in_grains}, "{self.deskr.text()}",
        {self.price.value()}, {self.volume.value()})''')
        con.commit()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mn = MainWindow()
    sys.excepthook = except_hook
    mn.show()
    sys.exit(app.exec())
