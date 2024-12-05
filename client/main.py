import sys

from PyQt6.QtWidgets import QApplication

from welcome.welcome_window_func import welcome_win


def my_exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)


def main():
    sys._excepthook = sys.excepthook
    sys.excepthook = my_exception_hook

    app = QApplication(sys.argv)
    w = welcome_win()
    w.show()
    print('Start app')
    app.exec()


if __name__ == '__main__':
    main()

example = {'nickname': 'mun', 'password': 'xxZxzxczxczcz'}
