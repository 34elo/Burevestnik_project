import datetime
import time
from datetime import datetime


def time_now():
    return f"{datetime.date.today()} {time.strftime('%H')}"


def compare_dates(date_str1, date_str2):
    date1 = datetime.strptime(date_str1, '%Y-%m-%d 00')
    date2 = datetime.strptime(date_str2, '%Y-%m-%d 00')
    if date1 < date2:
        return -1
    elif date1 == date2:
        return 0
    else:
        return 1


def calculate_time_difference(time_str1, time_str2):
    time_format = '%Y-%m-%d %H'
    if time_str2 is None:
        time_str2 = time_now()

    time2 = datetime.strptime(time_str2, time_format)
    time1 = datetime.strptime(time_str1, time_format)

    time_difference = abs((time1 - time2).total_seconds() // 3600)

    return int(time_difference)


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
        return None
    formatted_dates = [d.strftime('%Y-%m-%d') for d in dates]
    return formatted_dates
