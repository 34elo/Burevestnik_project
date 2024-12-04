import asyncio
import subprocess
from aiogram import Bot, Dispatcher
from server.settings import TOKEN

async def run_flask_server():
    process = subprocess.Popen(['python', 'flask_app.py', TOKEN]) # Передаём токен
    try:
        await asyncio.sleep(3600)
        process.terminate()
    except asyncio.CancelledError:
        process.terminate()
        pass

async def main():
    await asyncio.gather(
        # Не нужно запускать бота здесь, он запущен в flask_app.py
        run_flask_server()
    )

if __name__ == "__main__":
    asyncio.run(main())