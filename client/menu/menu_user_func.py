from http.client import responses
from turtledemo.penrose import start

import requests
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from client.menu import menu_user
from client.misc.func_with_time import time_now


def send_application(self, id_hardware, comment_applicant):
    start_time = time_now()
    repair_hardware = {'comment_applicant': comment_applicant,
                       'comment_work': None,
                       'done': 0,
                       'end': None,
                       'id_hardware': id_hardware,
                       'nickname': None,
                       'start': start_time}
    response = requests.post('http://127.0.0.1:5000/data/repair_hardware', json=repair_hardware)

def update_good_status(nickname):
    end_time = time_now()
    repair_hardware = {'done': 1,
                       'end': end_time,
                       'comment_work': 'No problems',
                       'nickname': nickname}
    user = {'nickname': nickname, 'busy': 0}
    response_repair_hardware_nickname = requests.get('http://127.0.0.1:5000/data/repair_hardware').json()
    for row in response_repair_hardware_nickname:
        if row.get('nickname') == nickname:
            id_repair_hardware = row.get('id')
            break

    response_repair_hardware = requests.put(f'http://127.0.0.1:5000/data/repair_hardware/{id_repair_hardware}',
                                            json=repair_hardware)
    response_users = requests.put(f'http://127.0.0.1:5000/data/users/{nickname}', json=user)

def update_bad_status(nickname, comment_worker):
    repair_hardware = {'done': 0,
                       'comment_work': comment_worker,
                       'nickname': None}
    user = {'nickname': nickname, 'busy': 0}
    response_repair_hardware_nickname = requests.get('http://127.0.0.1:5000/data/repair_hardware').json()
    id_repair_hardware = 0
    for row in response_repair_hardware_nickname:
        if row.get('nickname') == nickname:
            id_repair_hardware = row.get('id')
            break

    response_repair_hardware = requests.put(f'http://127.0.0.1:5000/data/repair_hardware/{id_repair_hardware}',
                                            json=repair_hardware)

    response_users = requests.put(f'http://127.0.0.1:5000/data/users/{nickname}', json=user)


class Ui_MainWindow2(QMainWindow, menu_user.Ui_MainWindow):
    # Класс основного окна пользователя
    def __init__(self, nickname):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('SideBar Menu')
        self.pushButton_link1.clicked.connect(self.open_link1)
        self.nickname = nickname

        # Подключение кнопок к их функционалу
        self.pushButton_education1us.clicked.connect(self.switch_to_money)
        self.pushButton_education2_us.clicked.connect(self.switch_to_money)

        self.pushButton_acc2_us.clicked.connect(self.switch_to_trackng)
        self.pushButton_acc1_us.clicked.connect(self.switch_to_trackng)

        self.pushButton_orde1_2.clicked.connect(self.switch_to_order)
        self.pushButton_order2_2.clicked.connect(self.switch_to_order)

        self.pushButton_send_order.clicked.connect(self.send_application)
        self.pushButton_send_order_2.clicked.connect(self.send_good_statement)
        self.pushButton_send_order_3.clicked.connect(self.send_bad_statement)
        self.widget_5.setHidden(True)
        self.account_page()

    def account_page(self):
        response = requests.get('http://127.0.0.1:5000/data/users').json()
        req: dict = {}
        for row in response:
            if row.get('nickname') == self.nickname:
                req = row

        self.label_nik.setText(str(req['nickname']))
        self.label_midlename.setText(str(req['middle_name']))
        self.label_secondnaame.setText(str(req['surname']))
        self.label_name.setText(str(req['name']))
        self.label_post.setText(str(req['post']))
        self.label_age.setText(str(req['age']))
        self.label_level.setText(str(req['skill_level']))
        self.label_exp.setText(str(req['experience']))

    def switch_to_money(self):
        self.stackedWidget.setCurrentIndex(0)  # Переключение на страницу "Деньги"

    def open_link1(self):
        url = QUrl("https://dpoprof.ru/povyshenie/povyshenie-kvalifikacii-tokar/")
        QDesktopServices.openUrl(url)

    def open_link2(self):
        url = QUrl("")
        QDesktopServices.openUrl(url)

    def open_link3(self):
        url = QUrl("")
        QDesktopServices.openUrl(url)

    def switch_to_trackng(self):
        self.stackedWidget.setCurrentIndex(1)  # Переключение на страницу "Отслеживание"

    def switch_to_order(self):
        self.stackedWidget.setCurrentIndex(2)  # Переключение на страницу "Заказ"

    def send_application(self):
        # Отправка деталей заявки в базу данных
        id_hardware = self.lineEdit_id_input.text()
        comment_applicant = self.textEdit_com_1.toPlainText()
        send_application(self, id_hardware, comment_applicant)  # Вызов функции для отправки заявки
        self.textEdit_com_1.clear()  # Очистка текстового поля комментария
        self.lineEdit_id_input.clear()  # Очистка текстового поля ввода ID оборудования

    def send_good_statement(self):
        update_good_status(self.nickname)  # Обновление статуса хороших ремонтов

    def send_bad_statement(self):
        comment_worker = self.textEdit_com_2.toPlainText()  # Получение комментария о плохом состоянии
        self.textEdit_com_2.clear()  # Очистка текстового поля комментария
        update_bad_status(self.nickname, comment_worker)  # Обновление статуса с плохим ремонтом
