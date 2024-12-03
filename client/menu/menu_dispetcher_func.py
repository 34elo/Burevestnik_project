import sys

import requests
from PyQt6.QtCore import QAbstractTableModel, Qt

from PyQt6.QtWidgets import QMainWindow, QMessageBox
from pyqtgraph import DateAxisItem

from client.menu import menu_dispetcher
from client.settings import API_URL

import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from datetime import datetime

from datetime import date, timedelta


def get_dates(period):
    today = date.today()

    if period == 'year':
        year_start = date(today.year, 1, 1)
        year_end = date(today.year, 12, 31)
        dates = [year_start + timedelta(days=x) for x in range((year_end - year_start).days + 1)]
    elif period == 'month':
        month_start = date(today.year, today.month, 1)
        next_month = month_start.replace(day=28) + timedelta(days=4)
        month_end = next_month - timedelta(days=next_month.day)
        dates = [month_start + timedelta(days=x) for x in range((month_end - month_start).days + 1)]
    elif period == 'week':
        start_of_week = today - timedelta(days=today.weekday())
        dates = [start_of_week + timedelta(days=x) for x in range(7)]
    else:
        return None  # Некорректный период
    formatted_dates = [d.strftime('%Y-%m-%d') for d in dates]
    return formatted_dates


def create_top_users(data):
    # Проверка наличия необходимых ключей
    required_keys = ['name', 'middle_name', 'surname', 'completed_task', 'post']
    for item in data:
        if not all(key in item for key in required_keys):
            print(f"Ошибка: Отсутствуют необходимые ключи в словаре: {item}")
            return None

    # Обработка completed_task (преобразование в число и обработка)
    for item in data:
        try:
            item['completed_task'] = int(item.get('completed_task', 0))
        except ValueError:
            pass

    # Сортировка пользователей по completed_task в убывающем порядке
    sorted_users = sorted(data, key=lambda x: x['completed_task'], reverse=True)

    # Создание списка названий столбцов
    columns = ['ФИО', 'Выполненные задания', 'Должность']

    # Создание списка строк
    rows = [[
        f"{user['name']} {user['middle_name']} {user['surname']}",
        user['completed_task'],
        user['post']
    ] for user in sorted_users]

    return columns, rows


def create_top_team(data):
    teams = {}
    for item in data:
        team_id = int(item['team'])
        if team_id not in teams:
            teams[team_id] = []
        teams[team_id].append(item)

    team_data = []
    for team_id, team_members in teams.items():

        completed_tasks = sum(int(item.get('completed_task', 0)) for item in team_members if
                              isinstance(item.get('completed_task'), (int, float)))
        try:
            best_worker = max(team_members, key=lambda x: x.get('completed_task', 0))
            best_worker_fio = f"{best_worker['name']} {best_worker['middle_name']} {best_worker['surname']}"
        except (ValueError, KeyError, TypeError):  # Обработка различных ошибок
            best_worker_fio = "N/A"
        team_data.append({'team': team_id, 'completed_tasks': completed_tasks, 'best_worker_fio': best_worker_fio})
    columns = ['team', 'completed_tasks', 'best_worker_fio']

    # Создание списка строк
    rows = [[str(item['team']), str(item['completed_tasks']), item['best_worker_fio']] for item in team_data]

    return columns, sorted(rows, key=lambda x: x[1], reverse=True)


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


class DateAxisItem(pg.AxisItem):  # Определение DateAxisItem здесь
    def tickStrings(self, values, scale, spacing):
        return [datetime.fromtimestamp(value).strftime('%Y-%m-%d') for value in values]


class Ui_MainWindow1(QMainWindow, menu_dispetcher.Ui_MainWindow):
    # Класс основного окна администратора
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.statistic = 'month'
        self.graphicsView_statistic.setBackground('w')
        # Подключение кнопок к соответствующим функциям
        self.pushButton_send_order.clicked.connect(self.send_order)
        self.refresh_btn.clicked.connect(self.refresh_bd)
        self.widget_5.setHidden(True)

        self.pushButton_tracing1.clicked.connect(self.switch_to_work)
        self.pushButton_tracing2.clicked.connect(self.switch_to_work)

        self.pushButton_team.clicked.connect(self.switch_to_top)
        self.pushButton_team2.clicked.connect(self.switch_to_top)

        self.pushButton_money1.clicked.connect(self.switch_to_statistic)
        self.pushButton_money2.clicked.connect(self.switch_to_statistic)

        self.pushButton_graph_4.clicked.connect(self.refresh_top_team)
        self.pushButton_graph_5.clicked.connect(self.refresh_top_users)

        self.pushButton_graph_6.clicked.connect(self.statistic_week)
        self.pushButton_graph_7.clicked.connect(self.statistic_month)
        self.pushButton_graph_9.clicked.connect(self.statistic_year)

        self.pushButton_graph.clicked.connect(self.build_graph)

    def statistic_year(self):
        self.statistic = 'year'
        print(self.statistic)

    def statistic_month(self):
        self.statistic = 'month'
        print(self.statistic)

    def statistic_week(self):
        self.statistic = 'week'
        print(self.statistic)

    def send_order(self):
        # Отправка информации о заказе в базу данных
        nik_work = self.lineEdit_nik_work.text()  # Получение ника работника
        id_problem = self.lineEdit_id_problem.text()  # Получение ID проблемы
        send_to_db(nik_work, id_problem, self)  # Отправка в базу данных

    def refresh_top_team(self):
        users = get_users()
        headers, rows = create_top_team(users)
        model_users = JsonTableModel(rows)
        model_users._headers = headers
        self.tableView_top_team.setModel(model_users)
        self.tableView_top_team.setStyleSheet("color: black; background-color: white;")

    def refresh_top_users(self):
        users = get_users()
        headers, rows = create_top_users(users)
        model_users = JsonTableModel(rows)
        model_users._headers = headers
        self.tableView_top_useres.setModel(model_users)
        self.tableView_top_useres.setStyleSheet("color: black; background-color: white;")

    def refresh_bd(self):
        users = get_users()
        repair_hardware = get_repair_hardware()
        headers = list(repair_hardware[0].keys())  # Заголовки из ключей первого словаря
        rows = [[row[header] for header in headers if row['done'] == 0] for row in repair_hardware]
        try:
            rows.remove([])
        except ValueError:
            pass
        model_users = JsonTableModel(rows)
        model_users._headers = headers
        self.tableView.setModel(model_users)
        self.tableView.setStyleSheet("color: black; background-color: white;")

        headers = list(users[0].keys())
        headers.remove('password')
        rows = [[row[header] for header in headers] for row in users]
        model_repair_hardware = JsonTableModel(rows)
        model_repair_hardware._headers = headers
        self.tableView_2.setModel(model_repair_hardware)
        self.tableView_2.setStyleSheet("color: black; background-color: white;")

    def switch_to_statistic(self):
        self.stackedWidget.setCurrentIndex(0)

    def switch_to_top(self):
        self.stackedWidget.setCurrentIndex(2)

    def switch_to_work(self):
        self.stackedWidget.setCurrentIndex(1)

    def build_graph(self):
        self.graphicsView_statistic.clear()
        repair_hardware = get_repair_hardware()
        # ("2024-01-01 00", 10)
        all_dates = get_dates(self.statistic)
        datas = [i for i in repair_hardware if i.get('done') == 1]
        data = []
        for i in all_dates:
            res = 0
            for j in datas:
                if j.get('end')[:10] == i:
                    res += 1
            data.append((i, res))
        print(data)
        print(self.statistic)
        x_data = [datetime.strptime(date_str.split()[0], '%Y-%m-%d').timestamp() for date_str, _ in data]
        y_data = [count for _, count in data]

        self.graphicsView_statistic.plot(x_data, y_data, pen='r', symbol='o')
        self.graphicsView_statistic.setLabel('left', 'Количество работы')
        self.graphicsView_statistic.setLabel('bottom', 'Дата')
        self.graphicsView_statistic.showGrid(x=True, y=True)
        self.graphicsView_statistic.setAxisItems({'bottom': DateAxisItem(orientation='bottom')})
        self.graphicsView_statistic.setTitle("Статистика выполненной работы")
