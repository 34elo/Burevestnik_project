import random

import requests
from PyQt6.QtWidgets import QMainWindow, QMessageBox

import client.register.register_window
from client.login.login_window_func import login_win


class register_win(QMainWindow, client.register.register_window.Ui_Dialog):
    # Класс окна регистрации
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_reg_reg.clicked.connect(self.registration)

    def registration(self):
        # Регистрация нового пользователя
        experience = self.lineEdit_expirience_reg.text()
        skill_level = self.lineEdit_level_reg.text()
        nickname = self.lineEdit_login_reg.text()
        middle_name = self.lineEdit_midlname_reg.text()
        password = self.lineEdit_paswword_reg.text()
        surname = self.lineEdit_secondname_reg.text()
        name = self.lineEdit_name_reg.text()
        post = self.lineEdit_post_reg.text()
        age = self.lineEdit_age_reg.text()
        team = random.randint(1,3)
        user = {'experience': experience, 'skill_level': skill_level, 'nickname': nickname, 'password': password, 'surname': surname, 'name': name, 'post': post, 'age': age, 'busy': 0, 'team': team, 'middle_name': middle_name}


        try:
            response = requests.post('http://127.0.0.1:5000/data/users', json=user)
            if response.status_code == 201:
                print('success register')
                self.window = login_win()
                self.window.show()
                self.close()
            else:
                print("Ошибка входа")
        except Exception as e:
            QMessageBox.critical(self, 'Critical', 'Прод упал, попробуйте позже')