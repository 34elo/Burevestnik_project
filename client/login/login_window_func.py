import sqlite3

import requests
from PyQt6.QtWidgets import QMainWindow, QMessageBox

import client.login.login_window
from client.menu.menu_dispetcher_func import Ui_MainWindow1
from client.menu.menu_user_func import Ui_MainWindow2


class login_win(QMainWindow, client.login.login_window.Ui_reg2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.pushButton_login_log.clicked.connect(self.login_in_system)

    def login_in_system(self):
        nickname_check = self.lineEdit_log_log.text()
        password_check = self.lineEdit_passwor_log.text()
        try:
            password = requests.post('http://127.0.0.1:5000/password', json={'password': password_check}).json()
            response = requests.get('http://127.0.0.1:5000/data/users')
        except Exception as e:
            print(e)
            QMessageBox.critical(self, 'Critical', 'Прод упал, попробуйте позже')
        password = password.get('password')

        for i in response.json():
            if i.get('nickname') == nickname_check and i.get('password') == password:
                print('User login')
                self.window = Ui_MainWindow2(nickname_check)  # Открывает основное окно для пользователя
                self.window.show()
                self.close()  # Закрывает окно входа

                return True
            elif nickname_check == 'admin' and password_check == 'admin':
                print('Admin login')
                self.window = Ui_MainWindow1()  # Открывает основное окно для пользователя
                self.window.show()
                self.close()  # Закрывает окно входа
                return True
        else:
            QMessageBox.critical(self, 'Ошибка', 'Неверный логин или пароль')
