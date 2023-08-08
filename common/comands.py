from aiogram import Dispatcher, types
from common.states.none_auth import NoneAuth
from common.states.access_states import StartMenu
from db.methods import db_exists_user


async def start(message: types.Message):
    user = await db_exists_user(message.from_user.id)
    if user:
        await message.answer(f"Здравствуйте {user[1]}!")
        await StartMenu.menu.set()
    else:
        await message.answer(
            f"Вас нет в базе. Обратитесь к администратору. "
            f"\n\nВаш id для регистрации: `{message.from_user.id}`",
            parse_mode="Markdown")


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start, state=[None, NoneAuth.start])
    dp.register_message_handler(start, commands=['menu', 'start'])
