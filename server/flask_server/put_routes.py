import sqlite3
from flask import request, jsonify
from server.misc.func_password import my_hash
from server.settings import DATABASE


def update_data_users(data_nickname):
    data = request.get_json()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    updates = []
    params = []

    if 'nickname' in data:
        updates.append("nickname = ?")
        params.append(data['nickname'])
    if 'password' in data:
        updates.append("password = ?")
        params.append(my_hash(data['password']))
    if 'middle_name' in data:
        updates.append("middle_name = ?")
        params.append(data['middle_name'])
    if 'surname' in data:
        updates.append("surname = ?")
        params.append(data['surname'])
    if 'name' in data:
        updates.append("name = ?")
        params.append(data['name'])
    if 'post' in data:
        updates.append("post = ?")
        params.append(data['post'])
    if 'age' in data:
        updates.append("age = ?")
        params.append(data['age'])
    if 'telegram' in data:
        updates.append("telegram = ?")
        params.append(data['telegram'])
    if 'skill_level' in data:
        updates.append("skill_level = ?")
        params.append(data['skill_level'])
    if 'experience' in data:
        updates.append("experience = ?")
        params.append(data['experience'])
    if 'busy' in data:
        updates.append("busy = ?")
        params.append(data['busy'])
    if 'team' in data:
        updates.append("team = ?")
        params.append(data['team'])
    if 'completed_task' in data:
        updates.append("completed_task = ?")
        params.append(data['completed_task'])

    if not updates:
        conn.close()
        return jsonify({'message': 'No fields to update'}), 400

    sql = f"UPDATE users SET {', '.join(updates)} WHERE nickname = ?"
    params.append(data_nickname)

    try:
        cursor.execute(sql, params)
        conn.commit()
        conn.close()
        return jsonify({'message': 'Data updated successfully'}), 200
    except sqlite3.Error as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': str(e)}), 500


def update_data_repair_hardware(data_id):
    data = request.get_json()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    updates = []
    params = []

    if 'nickname' in data:
        updates.append("nickname = ?")
        params.append(data['nickname'])
    if 'start' in data:
        updates.append("start = ?")
        params.append(data['start'])
    if 'end' in data:
        updates.append("end = ?")
        params.append(data['end'])
    if 'comment_work' in data:
        updates.append("comment_work = ?")
        params.append(data['comment_work'])
    if 'comment_applicant' in data:
        updates.append("comment_applicant = ?")
        params.append(data['comment_applicant'])
    if 'id_hardware' in data:
        updates.append("id_hardware = ?")
        params.append(data['id_hardware'])
    if 'done' in data:
        updates.append("done = ?")
        params.append(data['done'])

    if not updates:
        conn.close()
        return jsonify({'message': 'No fields to update'}), 400  # Или 204 No Content

    sql = f"UPDATE repair_hardware SET {', '.join(updates)} WHERE id = ?"
    params.append(data_id)  # Добавляем ID в конце

    cursor.execute(sql, params)
    conn.commit()
    conn.close()
    return jsonify({'message': 'Data updated successfully'}), 200


def update_data_hardware(data_id):
    data = request.get_json()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    updates = []
    params = []

    if 'name' in data:
        updates.append("name = ?")
        params.append(data['name'])
    if 'details' in data:
        updates.append("details = ?")
        params.append(data['details'])
    if 'type' in data:
        updates.append("type = ?")
        params.append(data['type'])
    if 'hard' in data:
        updates.append("hard = ?")
        params.append(data['hard'])
    if 'country' in data:
        updates.append("country = ?")
        params.append(data['country'])
    if 'year' in data:
        updates.append("year = ?")
        params.append(data['year'])
    if 'repair' in data:
        updates.append("repair = ?")
        params.append(data['repair'])

    if not updates:
        conn.close()
        return jsonify({'message': 'No fields to update'}), 400  # Или 204 No Content

    sql = f"UPDATE hardware SET {', '.join(updates)} WHERE id = ?"
    params.append(data_id)

    try:
        cursor.execute(sql, params)
        conn.commit()
        conn.close()
        return jsonify({'message': 'Data updated successfully'}), 200
    except sqlite3.Error as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': str(e)}),
