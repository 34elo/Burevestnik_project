from PyQt6.QtWidgets import QMainWindow

from client.menu import menu_dispetcher


def send_to_db(nik_work, id_problem):
    pass

    """UPDATE users SET busy = ? WHERE nickname = ?
    UPDATE repair_hardware SET nickname = ? WHERE id = ?"""


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
        send_to_db(nik_work, id_problem)  # Отправка в базу данных

    def refresh_bd(self):
        # Обновление данных, отображаемых в таблицах
        db = QSqlDatabase.addDatabase('QSQLITE')  # Указание типа базы данных
        db.setDatabaseName('db/tab.db')  # Установка имени базы данных
        db.open()  # Открытие соединения с базой данных

        # Создание модели для таблицы пользователей и установка её в представление таблицы
        model = QSqlTableModel(self, db)
        model.setTable('users')
        model.select()
        self.tableView_2.setModel(model)
        self.tableView_2.setStyleSheet("color: black; background-color: white;")

        # Создание модели для таблицы ремонтов и установка её в представление таблицы
        model = QSqlTableModel(self, db)
        model.setTable('repair_hardware')
        model.select()
        self.tableView.setModel(model)
        self.tableView.setStyleSheet("color: black; background-color: white;")
