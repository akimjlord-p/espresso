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
        for coffee_type in data:
            post = f'{coffee_type[0]}. {coffee_type[1]}: {coffee_type[2]} {coffee_type[3]} {coffee_type[4]} {coffee_type[5]} {coffee_type[6]}'
            self.coffeelist.addItem(post)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = CoffeeEspresso()
    form.show()
    sys.exit(app.exec())