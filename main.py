import logging
import os

from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from db import init_db
from elma.elma import elma

from common.states.access_states import *
from common.states.none_auth import *
from db.methods import *
from common.comands import access_management_menu

from common.comands import register_handlers_common

from access_management.list import register_handlers_access_management_list
from access_management.panel import register_handlers_access_management_panel
from access_management.add_new_user import register_handlers_access_management_add_new_user
from access_management.remove_user import register_handlers_access_management_remove_user

from company_indicators.panel import register_handlers_select_company_indicators
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
register_handlers_access_management_add_new_user(dp)
register_handlers_access_management_remove_user(dp)

register_handlers_select_company_indicators(dp)
###


# Удалить пользователя
@dp.message_handler(content_types=['text'], text='✅', state=FormRemoveUser.check)
async def remove_approved(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user = await db_exists_user(int(data['id']))
        if user:
            user_id = user[0]

            await db_remove_user(user_id)
            await state.reset_state()
            await PanelAccessManagement.menu.set()

            drop_state = dp.current_state(chat=user_id, user=user_id)
            await drop_state.set_state(NoneAuth.start)

            await message.answer("Пользователь удален")

        else:
            await message.answer("⚠️\nВидимо пользователя успели удалить до вашего запроса."
                                 "Обновите и проверьте список пользователей")

        return await access_management_menu(message)


############


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

