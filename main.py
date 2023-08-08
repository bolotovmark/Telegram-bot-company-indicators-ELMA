import logging
import os

from aiogram import Bot, Dispatcher, types, executor, filters
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from db import init_db
from elma.elma import elma

from common.comands import register_handlers_common

from access_management.list import register_handlers_access_management_list
from access_management.panel import register_handlers_access_management_panel

logging.basicConfig(level=logging.INFO)

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
bot = Bot(token=API_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Handlers
register_handlers_common(dp)
register_handlers_access_management_list(dp)
register_handlers_access_management_panel(dp)
###

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

