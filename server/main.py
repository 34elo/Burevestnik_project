import asyncio
import sqlite3
import sys
import threading

from aiogram import Bot, Dispatcher
from flask import Flask, request, jsonify
import aiohttp
from server.flask_server.get_routes import get_data_users, get_data_repair_hardware, get_data_hardware
from server.flask_server.post_routes import hash_password, add_data_users, add_data_repair_hardware, add_data_hardware
from server.flask_server.put_routes import update_data_users, update_data_repair_hardware, update_data_hardware
from server.settings import DATABASE, TOKEN
from server.telegramm.handlers import router

app = Flask(__name__)

bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(router)


async def telegram():
    await dp.start_polling(bot)
    print('fd')


app.add_url_rule('/password', view_func=hash_password, methods=['POST'])

app.add_url_rule('/data/users', view_func=get_data_users, methods=['GET'])
app.add_url_rule('/data/repair_hardware', view_func=get_data_repair_hardware, methods=['GET'])
app.add_url_rule('/data/hardware', view_func=get_data_hardware, methods=['GET'])

app.add_url_rule('/data/users', view_func=add_data_users, methods=['POST'])
app.add_url_rule('/data/hardware', view_func=add_data_hardware, methods=['POST'])
app.add_url_rule('/data/repair_hardware', view_func=add_data_repair_hardware, methods=['POST'])

app.add_url_rule('/data/users/<string:data_nickname>', view_func=update_data_users, methods=['PUT'])
app.add_url_rule('/data/repair_hardware/<int:data_id>', view_func=update_data_repair_hardware, methods=['PUT'])
app.add_url_rule('/data/hardware/<int:data_id>', view_func=update_data_hardware, methods=['PUT'])


async def send_telegram_message(user_id, message):
    try:
        await bot.send_message(chat_id=user_id, text=message)
        return {"success": True, "message": "Message sent successfully!"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}


async def handle_send_message(request):
    try:
        data = request.json()
        nickname = data.get('nickname')
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM users where nickname = ?", (nickname,)).fetchone()
        user_id = rows[7] if rows else None

        if user_id is None:
            return {"error": "User ID not found"}, 404

        message = 'У вас появилась новая работа'
        return await send_telegram_message(user_id, message)


    except ValueError as e:
        return {"error": str(e)}, 400
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        conn.close()


@app.route('/send_message', methods=['POST'])
async def send_message():
    async with aiohttp.ClientSession() as session:
        return jsonify(await handle_send_message(request))


def run_flask_server():
    app.run(port=5000, use_reloader=False)


if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask_server, daemon=True)
    flask_thread.start()
    asyncio.run(telegram())
