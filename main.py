import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog
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
        self.new_2.clicked.connect(self.add_or_update_new_post)
        self.from_db.clicked.connect(self.open_from_db)

    def add_or_update_new_post(self):
        if (self.name.text()
                and self.roasting.text()
                and self.grains.text()
                and self.description.text()
                and self.cost.text()
                and self.packag.text()):
            if not cur.execute(f'SELECT * FROM Coffee_info WHERE name="{self.name.text()}"').fetchall():
                cur.execute('SELECT id FROM Coffee_info WHERE id=(SELECT MAX(id) FROM Coffee_info)')
                last_id = cur.fetchone()
                if last_id:
                    id = int(last_id[0]) + 1
                else:
                    id = 0

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
                id = cur.execute(f'SELECT id FROM Coffee_info WHERE name="{self.name.text()}"').fetchone()
                cur.execute('UPDATE Coffee_info SET id=?, name=?, roasting=?, grains=?, description=?, cost=?, '
                            'packag=? WHERE name=?', (
                            id[0], self.name.text(), self.roasting.text(), self.grains.text(), self.description.text(),
                            self.cost.text(), self.packag.text(), self.name.text()))
                conn.commit()
                saved_msg = QMessageBox()
                saved_msg.setWindowTitle('Saved')
                saved_msg.setText("Updated into data base")
                saved_msg.setIcon(QMessageBox.Icon.Information)
                saved_msg.exec()
        else:
            error = QMessageBox()
            error.setWindowTitle('ERROR')
            error.setText('Incorrect input')
            error.setIcon(QMessageBox.Icon.Warning)
            error.exec()

    def open_from_db(self):
        posts = cur.execute("SELECT * FROM Coffee_info").fetchall()
        if len(posts) != 0:
            l = []
            for post in posts:
                l.append(f'{post[0]} {post[1]}')
            post, ok_pressed = QInputDialog.getItem(
                None, "Select post", "post:",
               l, 1, False)
            post = cur.execute('SELECT * FROM Coffee_info WHERE id=?', (post[0],)).fetchone()
            self.name.setText(post[1])
            self.roasting.setText(post[1])
            self.grains.setText(post[2])
            self.description.setText(post[3])
            self.cost.setText(post[4])
            self.packag.setText(post[5])
        else:
            saved_msg = QMessageBox()
            saved_msg.setWindowTitle('No projects')
            saved_msg.setText("No projects in local base")
            saved_msg.setIcon(QMessageBox.Icon.Information)
            saved_msg.exec()



def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = CoffeeEspresso()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
