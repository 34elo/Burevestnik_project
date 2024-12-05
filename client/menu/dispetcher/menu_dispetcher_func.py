from datetime import datetime

import requests
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from pyqtgraph import DateAxisItem

from client.exceptions import ReportException
from client.menu.DateAxisTime import DateAxisItem
from client.menu.JSONTableModel import JsonTableModel
from client.menu.dispetcher import menu_dispetcher
from client.menu.extra_func import get_users, get_repair_hardware
from client.menu.func_with_time import get_dates
from client.menu.report_funcs import docs_report, csv_report
from client.settings import API_URL


def create_top_users(data):
    required_keys = ['name', 'middle_name', 'surname', 'completed_task', 'post']
    for item in data:
        if not all(key in item for key in required_keys):
            print(f"Ошибка: Отсутствуют необходимые ключи в словаре: {item}")
            return None

    for item in data:
        try:
            item['completed_task'] = int(item.get('completed_task', 0))
        except ValueError:
            pass

    sorted_users = sorted(data, key=lambda x: x['completed_task'], reverse=True)
    columns = ['ФИО', 'Выполненные задания', 'Должность']

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
        except (ValueError, KeyError, TypeError):
            best_worker_fio = "N/A"
        team_data.append({'team': team_id, 'completed_tasks': completed_tasks, 'best_worker_fio': best_worker_fio})
    columns = ['team', 'completed_tasks', 'best_worker_fio']

    rows = [[str(item['team']), str(item['completed_tasks']), item['best_worker_fio']] for item in team_data]

    return columns, sorted(rows, key=lambda x: x[1], reverse=True)


def do_report(name, statistic, docs=True, csv=False):
    if docs:
        return docs_report(name, statistic)
    if csv:
        return csv_report(name, statistic)


def send_to_db(nickname, id_problem, self):  # Notification + send
    repair_hardware = {'nickname': nickname}
    user = {'nickname': nickname, 'busy': 1}
    response_repair_hardware_nickname = requests.get(f'{API_URL}/data/users').json()

    for row in response_repair_hardware_nickname:
        if row.get('nickname') == nickname:
            if row.get('busy') == 1:
                QMessageBox.critical(self, 'Critical', 'Работник уже занят, выберите другого')
                return

    requests.put(f'{API_URL}/data/repair_hardware/{id_problem}',
                 json=repair_hardware)
    requests.put(f'{API_URL}/data/users/{nickname}', json=user)


class Ui_MainWindow1(QMainWindow, menu_dispetcher.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.statistic = 'month'
        self.view()

    def view(self):
        self.pushButton_24.setHidden(True)
        self.graphicsView_statistic.setBackground('w')

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

        self.pushButton_report_2.clicked.connect(self.report)

    def build_graph(self):
        self.graphicsView_statistic.clear()
        repair_hardware = get_repair_hardware()
        all_dates = get_dates(self.statistic)
        datas = [i for i in repair_hardware if i.get('done') == 1]
        data = []
        for i in all_dates:
            res = 0
            for j in datas:
                if j.get('end')[:10] == i:
                    res += 1
            data.append((i, res))
        x_data = [datetime.strptime(date_str.split()[0], '%Y-%m-%d').timestamp() for date_str, _ in data]
        y_data = [count for _, count in data]

        self.graphicsView_statistic.plot(x_data, y_data, pen='r', symbol='o')
        self.graphicsView_statistic.setLabel('left', 'Количество работы')
        self.graphicsView_statistic.setLabel('bottom', 'Дата')
        self.graphicsView_statistic.showGrid(x=True, y=True)
        self.graphicsView_statistic.setAxisItems({'bottom': DateAxisItem(orientation='bottom')})
        self.graphicsView_statistic.setTitle("Статистика выполненной работы")

    def statistic_year(self):
        self.statistic = 'year'

    def statistic_month(self):
        self.statistic = 'month'

    def statistic_week(self):
        self.statistic = 'week'

    def send_order(self):
        nik_work = self.lineEdit_nik_work.text()
        id_problem = self.lineEdit_id_problem.text()
        send_to_db(nik_work, id_problem, self)

    def report(self):
        docs = self.radioButton_2.isChecked()
        csv = self.radioButton.isChecked()
        name = self.lineEdit.text()
        statistic = self.statistic
        if name == '':
            QMessageBox.critical(self, 'Critical', 'Заполни поля, дебил')
        else:
            try:
                message = do_report(name, statistic, csv=csv, docs=docs)
                QMessageBox.information(self, 'Успех', message)
            except ReportException:
                QMessageBox.critical(self, 'Critical', 'Error')

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
        print("refresh_db")
        users = get_users()
        repair_hardware = get_repair_hardware()

        try:
            headers = list(repair_hardware[0].keys())
            rows = [[row[header] for header in headers if
                     row['done'] == 0 and (row['nickname'] == "" or row['nickname'] is None)] for row in
                    repair_hardware]
        except IndexError:
            QMessageBox.warning(self, 'Error', 'Отсутсвуют данные')

        try:
            if [] in rows:
                while [] in rows:
                    rows.remove([])
        except ValueError:
            pass
        if not rows:
            print('not_rows')
            model_users = JsonTableModel([['']])
            model_users._headers = ['Отсутсвуют']
            self.tableView.setModel(model_users)
            self.tableView.setStyleSheet("color: black; background-color: white;")
        else:
            model_users = JsonTableModel(rows)
            model_users._headers = headers
            self.tableView.setModel(model_users)
            self.tableView.setStyleSheet("color: black; background-color: white;")

        headers = list(users[0].keys())
        headers.remove('password')
        rows = [[row[header] for header in headers if row['busy'] == 0] for row in users]
        try:
            if [] in rows:
                while [] in rows:
                    rows.remove([])
        except ValueError:
            pass
        if not rows:
            model_users = JsonTableModel([['']])
            model_users._headers = ['Отсутсвуют']
            self.tableView_2.setModel(model_users)
            self.tableView_2.setStyleSheet("color: black; background-color: white;")
        else:
            model_users = JsonTableModel(rows)
            model_users._headers = headers
            self.tableView_2.setModel(model_users)
            self.tableView_2.setStyleSheet("color: black; background-color: white;")

    def switch_to_statistic(self):
        self.stackedWidget.setCurrentIndex(0)

    def switch_to_top(self):
        self.stackedWidget.setCurrentIndex(2)

    def switch_to_work(self):
        self.stackedWidget.setCurrentIndex(1)
