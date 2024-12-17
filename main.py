import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
import sqlite3

conn = sqlite3.connect('coffee.sqlite')
cur = conn.cursor()


class CoffeeEspresso(QMainWindow):
    def __init__(self):
        super().__init__()
        f = open('main.ui', 'r')
        uic.loadUi(f, self)
        data = cur.execute('SELECT * from Coffee_info').fetchall()
        #for coffee_type in data:
        #    post = ''
        #    self.coffeelist.addItems(str(coffee_type))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = CoffeeEspresso()
    form.show()
    sys.exit(app.exec())