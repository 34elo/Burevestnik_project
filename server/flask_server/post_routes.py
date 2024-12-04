import asyncio
import sqlite3
from flask import request, jsonify

from server.misc.func_password import my_hash
from server.settings import DATABASE


def add_data_users():
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
    completed_task = data.get('completed_task')

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (nickname, password, middle_name, surname, name, post, age, telegram, skill_level, experience, busy, team, completed_task) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (nickname, password, middle_name, surname, name, post, age, telegram, skill_level, experience, busy, team,
         completed_task))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Data added successfully'}), 201


def add_data_repair_hardware():
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
    cursor.execute(
        "INSERT INTO repair_hardware (nickname, start, end, comment_work, comment_applicant, id_hardware, done) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (nickname, start, end, comment_work, comment_applicant, id_hardware, done))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Good'}), 201


def add_data_hardware():
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
    cursor.execute(
        "INSERT INTO repair_hardware (name, details, type, hard, country, year, repair) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (name, details, type, hard, country, year, repair))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Good'}), 201


def hash_password():
    password_from_user = request.get_json()
    password_from_user = password_from_user.get('password')
    password = my_hash(password_from_user)
    return jsonify({'password': password})
