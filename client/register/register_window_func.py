import random

import requests
from PyQt6.QtWidgets import QMainWindow, QMessageBox

import client.register.register_window
from client.login.login_window_func import login_win
from client.settings import API_URL


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
        if experience and skill_level and nickname and middle_name and password and surname and name and post and age:
            team = random.randint(1, 3)
            user = {'experience': experience, 'skill_level': skill_level, 'nickname': nickname, 'password': password,
                    'surname': surname, 'name': name, 'post': post, 'age': age, 'busy': 0, 'team': team,
                    'middle_name': middle_name}
            try:
                response = requests.post(f'{API_URL}/data/users', json=user)
                self.window = login_win()
                self.window.show()
                self.close()
            except Exception as e:
                print(e)
                QMessageBox.critical(self, 'Critical', 'Прод упал, попробуйте позже')
        else:
            QMessageBox.critical(self, 'Critical', 'Вы ввели не все данные')