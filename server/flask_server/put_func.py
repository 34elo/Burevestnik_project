import sqlite3
from flask import request, jsonify

from server.main import app
from server.misc.func_password import my_hash
from server.settings import DATABASE


@app.route('/data/users/<string:data_nickname>', methods=['PUT'])
def update_data_users(data_nickname):
    data = request.get_json()
    nickname = data.get('nickname')
    password = my_hash(data.get('password'))
    middle_name = data.get('middle_name')
    surname = data.get('surname')
    name = data.get('name')
    post = data.get('post')
    age = data.get('age')
    telegram = data.get('telegram')
    skill_level = data.get('skill_level')
    experience = data.get('experience')
    busy = data.get('busy')
    team = data.get('team')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET nickname = ?, password = ?, middle_name = ?, surname = ?, name = ?, post = ?, age = ?, telegram = ?, skill_level = ?, experience = ?, busy = ?, team = ? WHERE nickname = ?",
                   (nickname, password, middle_name, surname, name, post, age, telegram, skill_level, experience, busy, team, data_nickname))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Update is good'}), 400


@app.route('/data/repair_hardware/<int:data_id>', methods=['PUT'])
def update_data_repair_hardware(data_id):
    data = request.get_json()
    nickname = data.get('nickname')
    start = data.get('start')
    end = data.get('end')
    comment_work = data.get('comment_work')
    comment_applicant = data.get('comment_applicant')
    id_hardware = data.get('id_hardware')
    done = data.get('done')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE repair_hardware SET nickname = ?, start = ?, end = ?, comment_work = ?, comment_applicant = ?, id_hardware = ?, done = ? WHERE id = ?",
                   (nickname, start, end, comment_work, comment_applicant, id_hardware, done, data_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Update is good'}), 400


@app.route('/data/hardware/<int:data_id>', methods=['PUT'])
def update_data_hardware(data_id):
    data = request.get_json()
    name = data.get('name')
    details = data.get('details')
    type = data.get('type')
    hard = data.get('hard')
    country = data.get('country')
    year = data.get('year')
    repair = data.get('repair')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE hardware SET name = ?, details = ?, type = ?, hard = ?, country = ?, year = ?, repair = ? WHERE id = ?",
                   (name, details, type, hard, country, year, repair, data_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Update is good'}), 400


