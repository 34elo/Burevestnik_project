import requests
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from client.menu.extra_func import get_task, get_have_task, send_application
from client.menu.func_with_time import time_now
from client.menu.user import menu_user
from client.settings import API_URL


def update_good_status(self, nickname):
    end_time = time_now()
    repair_hardware = {'done': 1,
                       'end': end_time,
                       'comment_work': 'No problems',
                       'nickname': nickname}
    user = {'nickname': nickname, 'busy': 0}
    response_repair_hardware_nickname = requests.get(f'{API_URL}/data/repair_hardware').json()
    id_repair_hardware_ = 0
    for row in response_repair_hardware_nickname:
        if row.get('nickname') == nickname:
            id_repair_hardware_ = row.get('id')
            break

    if id_repair_hardware_ == 0:
        QMessageBox.critical(self, "Error", 'У тебя нет задач')
    else:

        response_repair_hardware = requests.put(f'{API_URL}/data/repair_hardware/{id_repair_hardware_}',
                                                json=repair_hardware)
        response_users = requests.put(f'{API_URL}/data/users/{nickname}', json=user)
        QMessageBox.information(self, "Success", 'Успех')


def update_bad_status(self, nickname, comment_worker):
    repair_hardware = {'done': 0,
                       'comment_work': comment_worker,
                       'nickname': None}
    user = {'nickname': nickname, 'busy': 0}
    response_repair_hardware_nickname = requests.get(f'{API_URL}/data/repair_hardware').json()
    id_repair_hardware_ = 0
    for row in response_repair_hardware_nickname:
        if row.get('nickname') == nickname and row.get('done') == 0:
            id_repair_hardware_ = row.get('id')
            break
    if id_repair_hardware_ == 0:
        QMessageBox.critical(self, "Error", 'У тебя нет задач')
    else:
        response_repair_hardware = requests.put(f'{API_URL}/data/repair_hardware/{id_repair_hardware_}',
                                                json=repair_hardware)

        response_users = requests.put(f'{API_URL}/data/users/{nickname}', json=user)
        QMessageBox.information(self, "Success", 'Успех')


class Ui_MainWindow2(QMainWindow, menu_user.Ui_MainWindow):
    def __init__(self, nickname):
        super().__init__()
        self.nickname = nickname
        self.setupUi(self)
        self.setWindowTitle('SideBar Menu')
        self.view()
        self.account_page()
        self.update_task()

    def view(self):
        self.pushButton_link1.clicked.connect(self.open_link1)
        self.label_nick2.setText(self.nickname)
        self.label_nick.setText(self.nickname)

        self.pushButton_education1us.clicked.connect(self.switch_to_money)
        self.pushButton_education2_us.clicked.connect(self.switch_to_money)

        self.pushButton_acc2_us.clicked.connect(self.switch_to_trackng)
        self.pushButton_acc1_us.clicked.connect(self.switch_to_trackng)

        self.pushButton_tasks2.clicked.connect(self.switch_to_notifications)
        self.pushButton_task1.clicked.connect(self.switch_to_notifications)

        self.pushButton_orde1_2.clicked.connect(self.switch_to_order)
        self.pushButton_order2_2.clicked.connect(self.switch_to_order)

        self.pushButton_send_order.clicked.connect(self.send_application)
        self.pushButton_send_order_sucses.clicked.connect(
            self.send_good_statement)
        self.pushButton_send_order_unsucses.clicked.connect(
            self.send_bad_statement)
        self.pushButton_update_task.clicked.connect(self.update_task)
        self.widget_5.setHidden(True)

    def update_task(self):
        if get_have_task(self.nickname):
            information = get_task(self.nickname)
            self.label_38.setText(
                "У вас есть задание, которое необходимо выполнить. Ниже приведена информация, которая поможет вам при её выполнении")
            self.label_number_machine.setText(str(information.get(str('id_hardware'))))
            self.label_coment_disp.setText(str(information.get(str('comment_applicant'))))
            self.frame_2.setHidden(True)
            self.frame.setHidden(False)

            return
        self.label_38.setText("У вас сейчас нет задания")
        self.label_number_machine.setText('-')
        self.label_coment_disp.setText('-')
        self.frame_2.setHidden(False)
        self.frame.setHidden(True)

    def account_page(self):
        response = requests.get(f'{API_URL}/data/users').json()
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
        self.stackedWidget.setCurrentIndex(0)

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
        self.stackedWidget.setCurrentIndex(1)

    def switch_to_order(self):
        self.stackedWidget.setCurrentIndex(2)

    def switch_to_notifications(self):
        self.stackedWidget.setCurrentIndex(3)

    def send_application(self):
        id_hardware = self.lineEdit_id_input.text()
        comment_applicant = self.textEdit_com_1.toPlainText()
        send_application(id_hardware, comment_applicant)
        self.textEdit_com_1.clear()
        self.lineEdit_id_input.clear()

    def send_good_statement(self):
        update_good_status(self, self.nickname)

    def send_bad_statement(self):
        comment_worker = self.textEdit_com__unsucses.toPlainText()
        update_bad_status(self, self.nickname, comment_worker)
        self.textEdit_com__unsucses.clear()
