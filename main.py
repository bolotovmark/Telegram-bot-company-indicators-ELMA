import logging
import os

from aiogram import Bot, Dispatcher, types, executor, filters
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from db import init_db

logging.basicConfig(level=logging.INFO)

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
bot = Bot(token=API_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

