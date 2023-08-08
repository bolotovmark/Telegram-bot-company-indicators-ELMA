from aiogram import Dispatcher, types
from common.states.access_states import PanelAccessManagement
from db.methods import db_get_list_user


# @dp.message_handler(content_types=['text'], text='Список пользователей', state=FormChangeListUsers)
async def list_users(message: types.Message):
    users = await db_get_list_user()
    for data in users:
        await message.answer(f"*{data[1]}*\n"
                             f"ID: `{data[0]}`", parse_mode="MarkdownV2")


def register_handlers_access_management_list(dp: Dispatcher):
    dp.register_message_handler(list_users, content_types=['text'], text='Список пользователей',
                                state=PanelAccessManagement)