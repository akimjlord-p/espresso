import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6 import uic
import sqlite3

conn = sqlite3.connect('coffee.sqlite')
cur = conn.cursor()


class CoffeeEspresso(QMainWindow):
    def __init__(self):
        super().__init__()
        self.new_des_window = None
        f = open('main.ui', 'r')
        uic.loadUi(f, self)
        data = cur.execute('SELECT * from Coffee_info').fetchall()
        self.posted = []
        for coffee_type in data:
            self.posted.append(coffee_type)
            post = f'{coffee_type[0]}. {coffee_type[1]}: {coffee_type[2]}; {coffee_type[3]}; {coffee_type[4]}; {coffee_type[5]}; {coffee_type[6]}'
            self.coffeelist.addItem(post)

        self.refresh.clicked.connect(self.refresh_list)
        self.des.clicked.connect(self.open_new_post_window)

    def refresh_list(self):
        data = cur.execute('SELECT * from Coffee_info').fetchall()
        for coffee_type in data:
            if coffee_type not in self.posted:
                post = f'{coffee_type[0]}. {coffee_type[1]}: {coffee_type[2]}; {coffee_type[3]}; {coffee_type[4]}; {coffee_type[5]}; {coffee_type[6]}'
                self.coffeelist.addItem(post)

    def open_new_post_window(self):
        self.new_des_window = NewPost()
        self.new_des_window.show()


class NewPost(QMainWindow):
    def __init__(self):
        super().__init__()
        f = open('addEditCoffeeForm.ui', 'r')
        uic.loadUi(f, self)
        self.new_2.clicked.connect(self.add_new_post)

    def add_new_post(self):
        cur.execute('SELECT id FROM Coffee_info WHERE id=(SELECT MAX(id) FROM Coffee_info)')
        last_id = cur.fetchone()
        if last_id:
            id = int(last_id[0]) + 1
        else:
            id = 0
        if (self.name.text()
                and self.roasting.text()
                and self.grains.text()
                and self.description.text()
                and self.cost.text()
                and self.packag.text()):
            cur.execute('INSERT INTO Coffee_info '
                        '(id, name, roasting, grains, description, cost, packag) VALUES(?, ?, ?, ?, ?, ?, ?)', (
                            id, self.name.text(), self.roasting.text(), self.grains.text(), self.description.text(),
                            self.cost.text(), self.packag.text()))
            conn.commit()
            saved_msg = QMessageBox()
            saved_msg.setWindowTitle('Saved')
            saved_msg.setText("Saved into data base")
            saved_msg.setIcon(QMessageBox.Icon.Information)
            saved_msg.exec()
        else:
            error = QMessageBox()
            error.setWindowTitle('ERROR')
            error.setText('Incorrect input')
            error.setIcon(QMessageBox.Icon.Warning)
            error.exec()

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = CoffeeEspresso()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
