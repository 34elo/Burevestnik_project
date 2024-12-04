import threading
import asyncio

from aiogram.dispatcher import router
from flask import Flask, request
from aiogram import Bot, Dispatcher

import asyncio
import sqlite3

from aiogram import Bot, Dispatcher
from flask import request, jsonify
from server.settings import DATABASE, TOKEN
from server.telegramm.handlers import router
from server.flask_server.get_routes import get_data_users, get_data_hardware, get_data_repair_hardware
from server.flask_server.post_routes import add_data_users, add_data_hardware, hash_password
from server.flask_server.put_routes import update_data_users, update_data_repair_hardware, update_data_hardware
from telegramm.handlers import router

from settings import TOKEN

app = Flask(__name__)

botinok = None  # make it global
app.add_url_rule('/password', view_func=hash_password, methods=['POST'])

app.add_url_rule('/data/users', view_func=get_data_users, methods=['GET'])
app.add_url_rule('/data/repair_hardware', view_func=get_data_repair_hardware, methods=['GET'])
app.add_url_rule('/data/hardware', view_func=get_data_hardware, methods=['GET'])

app.add_url_rule('/data/users', view_func=add_data_users, methods=['POST'])
app.add_url_rule('/data/hardware', view_func=add_data_hardware, methods=['POST'])
app.add_url_rule('/data/repair_hardware', view_func=add_data_hardware, methods=['POST'])

app.add_url_rule('/data/users/<string:data_nickname>', view_func=update_data_users, methods=['PUT'])
app.add_url_rule('/data/repair_hardware/<int:data_id>', view_func=update_data_repair_hardware, methods=['PUT'])
app.add_url_rule('/data/hardware/<int:data_id>', view_func=update_data_hardware, methods=['PUT'])

botinok = None


async def start_bot():
    global botinok  # access global variable
    botinok = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(botinok)

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    nickname = data.get('nickname')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM users where nickname = ?", (nickname,)).fetchone()
    user_id = rows[7]
    message = 'У вас появилась новая работа'
    if user_id == '' or user_id is None:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(botinok.send_message(chat_id=user_id, text=message))
            return jsonify({"success": True, "message": "Message sent successfully!"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return 0


if __name__ == "__main__":
    flask_thread = threading.Thread(target=lambda: app.run(port=5000), daemon=True)
    flask_thread.start()
    asyncio.run(start_bot())
