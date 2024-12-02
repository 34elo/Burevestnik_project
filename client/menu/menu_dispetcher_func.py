import sys

import requests
from PyQt6.QtCore import QAbstractTableModel, Qt

from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTableView, QVBoxLayout
import json

from PyQt6.uic.properties import QtWidgets

from client.menu import menu_dispetcher
from client.settings import API_URL


def get_users():
    response_users = requests.get(f'{API_URL}/data/users').json()
    return response_users


def get_repair_hardware():
    response_repair_hardware = requests.get(f'{API_URL}/data/repair_hardware').json()
    return response_repair_hardware


def send_to_db(nickname, id_problem, self):
    repair_hardware = {'nickname': nickname}
    user = {'nickname': nickname, 'busy': 1}
    response_repair_hardware_nickname = requests.get(f'{API_URL}/data/users').json()

    for row in response_repair_hardware_nickname:
        if row.get('nickname') == nickname:
            if row.get('busy') == 1:
                QMessageBox.critical(self, 'Critical', 'Работник уже занят, выберите другого')
                break

    response_repair_hardware = requests.put(f'{API_URL}/data/repair_hardware/{id_problem}',
                                            json=repair_hardware)
    response_users = requests.put(f'{API_URL}/data/users/{nickname}', json=user)
    """UPDATE users SET busy = ? WHERE nickname = ?
    UPDATE repair_hardware SET nickname = ? WHERE id = ?"""


class JsonTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        if self._data:
            return len(self._data[0])
        return 0

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section] if self._headers else str(section)
            else:
                return str(section)
        return None


class Ui_MainWindow1(QMainWindow, menu_dispetcher.Ui_MainWindow):
    # Класс основного окна администратора
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Подключение кнопок к соответствующим функциям
        self.pushButton_send_order.clicked.connect(self.send_order)
        self.refresh_btn.clicked.connect(self.refresh_bd)
        self.widget_5.setHidden(True)

    def send_order(self):
        # Отправка информации о заказе в базу данных
        nik_work = self.lineEdit_nik_work.text()  # Получение ника работника
        id_problem = self.lineEdit_id_problem.text()  # Получение ID проблемы
        send_to_db(nik_work, id_problem, self)  # Отправка в базу данных

    def refresh_bd(self):
        users = get_users()
        repair_hardware = get_repair_hardware()
        headers = list(users[0].keys())  # Заголовки из ключей первого словаря
        rows = [[row[header] for header in headers] for row in users]
        model_users = JsonTableModel(rows)
        model_users._headers = headers
        self.tableView.setModel(model_users)
        self.tableView.setStyleSheet("color: black; background-color: white;")

        headers = list(repair_hardware[0].keys())  # Заголовки из ключей первого словаря
        rows = [[row[header] for header in headers] for row in repair_hardware]
        model_repair_hardware = JsonTableModel(rows)
        model_repair_hardware._headers = headers
        self.tableView_2.setModel(model_repair_hardware)
        self.tableView_2.setStyleSheet("color: black; background-color: white;")