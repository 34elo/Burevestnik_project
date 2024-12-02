import requests

new_data = {'age': 25, 'busy': 0, 'experience': 5, 'middle_name': 'Васильевич', 'name': 'Максим', 'nickname': 'mun',
            'password': 'xxZxzxczxczcz', 'post': 'Инженер', 'skill_level': 6, 'surname': 'Кириллов', 'team': 1,
            'telegram': None}


def post():
    response = requests.post('http://127.0.0.1:5000/data/users', json=new_data)
    print(response.json())
    if response.status_code == 201:
        print("Данные успешно добавлены")
    else:
        print("Ошибка при добавлении данных:", response.json())


def get():
    response = requests.get('http://127.0.0.1:5000/data/users').json()
    print(response)
    nickname = 'vava'
    for row in response:
        if row.get('nickname') == nickname:
            req = row
    print(str(req.get('nickname')))
    print(str(req['nickname']))
    return response


def put():
    response = requests.put('http://127.0.0.1:5000/data/users/ben', json=new_data)


get()