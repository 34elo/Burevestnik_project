import threading
import asyncio

from aiogram.dispatcher import router
from flask import Flask
from aiogram import Bot, Dispatcher
from telegramm.handlers import router

from settings import TOKEN

app = Flask(__name__)

from flask_server.get_func import *
from flask_server.put_func import *
from flask_server.post_func import *
from flask_server.delete_func import *


async def start_bot():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


def run_flask():
    app.run(port=5000)


if __name__ == "__main__":
    # Запуск Flask
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    # Запуск Telegramm
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        print("Telegramm-bot off")
