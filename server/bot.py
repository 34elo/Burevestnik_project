import asyncio
import sqlite3

from aiogram import Bot, Dispatcher
from flask import request, jsonify

from server.main import botinok
from server.settings import DATABASE, TOKEN
from server.telegramm.handlers import router

botinok = None

async def start_bot():
    global botinok  # access global variable
    botinok = Bot(token=TOKEN)
    dp = Dispatcher(botinok)
    dp.include_router(router)
    await dp.start_polling()

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
