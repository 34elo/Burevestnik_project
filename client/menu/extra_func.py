import requests

from client.menu.func_with_time import time_now
from client.settings import API_URL


def send_application(id_hardware, comment_applicant):
    start_time = time_now()
    repair_hardware = {'comment_applicant': comment_applicant,
                       'comment_work': None,
                       'done': 0,
                       'end': None,
                       'id_hardware': id_hardware,
                       'nickname': None,
                       'start': start_time}
    response = requests.post(f'{API_URL}/data/repair_hardware', json=repair_hardware)


def get_users():
    response_users = requests.get(f'{API_URL}/data/users').json()
    return response_users


def get_repair_hardware():
    response_repair_hardware = requests.get(f'{API_URL}/data/repair_hardware').json()
    return response_repair_hardware


def get_task(nickname):
    response = requests.get(f'{API_URL}/data/repair_hardware').json()
    datas = {}
    for i in response:
        if i.get('nickname') == nickname:
            datas = i

    return datas


def get_have_task(nickname):
    response = requests.get(f'{API_URL}/data/repair_hardware').json()
    for i in response:
        if i.get("nickname") == nickname and i.get('done') == 0:
            return True
    return False


def get_good_dates_repair_hardware(dates, in_dates):
    result = []
    for i in dates:
        if i.get('start')[:10] in in_dates:
            result.append(i)
    return result
