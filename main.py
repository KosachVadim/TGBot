import asyncio
from aiogram import Dispatcher, Bot
from dotenv import load_dotenv
import os
from core.handlers.basic import router



async def start():
    load_dotenv()

    bot = Bot(token=os.getenv('TOKEN'))

    dp = Dispatcher()

    dp.include_router(router)

    try:
        await dp.start_polling(bot)

    finally:
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print('Exit')