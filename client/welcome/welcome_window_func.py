from PyQt6.QtWidgets import QMainWindow

import client.welcome.welcome_window
from client.login.login_window_func import login_win
from client.register.register_window_func import register_win


class welcome_win(QMainWindow, client.welcome.welcome_window.Ui_Dialog):
    # Класс диалогового окна регистрации
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Настройка интерфейса из файла дизайна
        # Подключение кнопок к соответствующим функциям
        self.pushButton_login_reg.clicked.connect(self.to_login)
        self.pushButton_registration.clicked.connect(self.to_registration)

    def to_login(self):
        # Открытие окна входа
        self.window = login_win()
        self.window.show()
        self.close()  # Закрывает окно регистрации

    def to_registration(self):
        # Открытие окна регистрации
        self.window = register_win()
        self.window.show()
        self.close()  # Закрывает окно регистрации
