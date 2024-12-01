from datetime import datetime  # Импорт модуля для работы с датами и временем
import time  # Импорт модуля для работы с временем


def time_now():
    # Функция возвращает текущее время в формате 'YYYY-MM-DD HH'
    import datetime  # Импортируем datetime для получения текущей даты
    return f"{datetime.date.today()} {time.strftime('%H')}"  # Возврат текущей даты с часом


# Функция для расчета времени в часах между двумя временными строками
def calculate_time_difference(time_str1, time_str2):
    time_format = '%Y-%m-%d %H'  # Определяем формат времени для парсинга
    if time_str2 is None:
        # Если вторая временная строка не передана, используем текущее время
        time_str2 = time_now()

    # Преобразуем строковые представления времени в объекты datetime
    time2 = datetime.strptime(time_str2, time_format)
    time1 = datetime.strptime(time_str1, time_format)

    # Вычисляем абсолютное значение разности во времени в секундах, затем конвертируем в часы
    time_difference = abs((time1 - time2).total_seconds() // 3600)

    return int(time_difference)  # Возвращаем разницу в часах как целое число