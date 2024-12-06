from PyQt6.QtWidgets import QMainWindow

import client.welcome.welcome_window
from client.login.login_window_func import login_win
from client.register.register_window_func import register_win


class welcome_win(QMainWindow, client.welcome.welcome_window.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_login_reg.clicked.connect(self.to_login)
        self.pushButton_registration.clicked.connect(self.to_registration)

    def to_login(self):
        self.window = login_win()
        self.window.show()
        self.close()

    def to_registration(self):
        self.window = register_win()
        self.window.show()
        self.close()
