from aiogram import Dispatcher, types
from common.states.none_auth import NoneAuth
from common.states.access_states import StartMenu
from db.methods import db_exists_user
from elma.elma import elma
from common.keyboards.static import start_menu


async def start(message: types.Message):
    user = await db_exists_user(message.from_user.id)
    if user:
        await message.answer(f"Здравствуйте {user[1]}!", reply_markup=start_menu)
        await StartMenu.menu.set()
    else:
        await message.answer(
            f"Вас нет в базе. Обратитесь к администратору. "
            f"\n\nВаш id для регистрации: `{message.from_user.id}`",
            parse_mode="Markdown")


async def revenue(message: types.Message):
    out = elma.elma_requests_QueryTree('7414f89e-b840-4137-8256-3ad2c6213816',
                                       "Name = ’Выручка, без НДС’",
                                       "Name,Summa,Kommentariy")

    await message.answer(f"*Показатель*: {out[0].Items[2].Value}\n"
                         f"*Значение*: {out[0].Items[3].Value}\n"
                         f"*Комментарий*: {out[0].Items[4].Value}", parse_mode='Markdown')


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start, state=[None, NoneAuth.start])
    dp.register_message_handler(start, commands=['menu', 'start'])

    dp.register_message_handler(revenue,
                                content_types=['text'],
                                text='Выручка',
                                state=StartMenu.menu)
