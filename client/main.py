import sys

from PyQt6.QtWidgets import QApplication
from welcome.welcome_window_func import welcome_win

def my_exception_hook(exctype, value, traceback):
    # Обработчик исключений, который выводит информацию об исключении и завершает приложение
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

def main():
    sys._excepthook = sys.excepthook
    sys.excepthook = my_exception_hook

    app = QApplication(sys.argv)  # Инициализация приложения
    w = welcome_win()  # Создание экземпляра начального окна регистрации
    w.show()  # Показ окна
    app.exec()  # Запуск цикла приложения
    global nickname


if __name__ == '__main__':
    main()

example = {'nickname': 'mun', 'password': 'xxZxzxczxczcz'}