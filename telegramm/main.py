import asyncio

import requests
from aiogram import Bot, Dispatcher
from server.settings import TOKEN, API_URL
from telegramm.handlers import router

bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(router)


async def send_request_to_server():
    try:
        data = requests.get(f'{API_URL}/send_message').json()
        print(data)
        for i in data:
            user_id = i[0]
            nickname = i[1]
            await bot.send_message(user_id, f'У вас появилась новая работа, {nickname}')

    except Exception as e:
        print(e)


async def scheduled_task():
    while True:
        await send_request_to_server()
        await asyncio.sleep(10)


async def telegram():
    await dp.start_polling(bot)


async def main():
    await asyncio.gather(telegram(), scheduled_task())


if __name__ == '__main__':
    asyncio.run(main())
