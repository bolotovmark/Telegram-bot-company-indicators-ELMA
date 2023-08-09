from aiogram import Dispatcher, types
from common.states.none_auth import NoneAuth
from common.states.access_states import StartMenu, PanelAccessManagement
from db.methods import db_exists_user
from elma.elma import elma
from common.keyboards.static import kb_start_menu, kb_access_management_menu


async def start(message: types.Message):
    user = await db_exists_user(message.from_user.id)
    if user:
        await message.answer(f"Здравствуйте {user[1]}!", reply_markup=kb_start_menu)
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

    await message.answer(f"*{out[0].Items[2].Value}*\n\n"
                         f"*Цифра:* {out[0].Items[3].Value}\n"
                         f"*Комментарий:* {out[0].Items[4].Value}", parse_mode='Markdown')


async def resource_plan(message: types.Message):
    out = elma.elma_requests_QueryTree('7414f89e-b840-4137-8256-3ad2c6213816',
                                       "Name = ’План поступления’",
                                       "Name,Summa,Kommentariy")

    await message.answer(f"*{out[0].Items[2].Value}*\n\n"
                         f"*Цифра:* {out[0].Items[3].Value}\n"
                         f"*Комментарий:* {out[0].Items[4].Value}", parse_mode='Markdown')


async def cost_effectiveness(message: types.Message):
    out = elma.elma_requests_QueryTree('7414f89e-b840-4137-8256-3ad2c6213816',
                                       "Name = ’Рентабельность’",
                                       "Name,Summa,Kommentariy")

    await message.answer(f"*{out[0].Items[2].Value}*\n\n"
                         f"*Цифра:* {out[0].Items[3].Value}\n"
                         f"*Комментарий:* {out[0].Items[4].Value}", parse_mode='Markdown')


async def start_menu(message: types.Message):
    await message.answer("Для навигации используйте панель", reply_markup=kb_start_menu)


async def access_management_menu(message: types.Message):
    await PanelAccessManagement.menu.set()
    await message.answer("Панель управления доступом", reply_markup=kb_access_management_menu)


async def cancel_access_management_menu(message: types.Message):
    await StartMenu.menu.set()
    return await start_menu(message)


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start, state=[None, NoneAuth.start])
    dp.register_message_handler(start, commands=['menu', 'start'])

    dp.register_message_handler(start_menu,
                                lambda message:
                                message.text not in ["📊 Показатели", "🪪 Управление доступом"],
                                state=StartMenu.menu)

    dp.register_message_handler(access_management_menu,
                                content_types=['text'],
                                text='🪪 Управление доступом',
                                state=StartMenu.menu)

    dp.register_message_handler(cancel_access_management_menu,
                                content_types=['text'],
                                text='↩️ Вернуться в главное меню',
                                state=[PanelAccessManagement])

    dp.register_message_handler(revenue,
                                content_types=['text'],
                                text='Выручка',
                                state=StartMenu.menu)

    dp.register_message_handler(resource_plan,
                                content_types=['text'],
                                text='План поступления',
                                state=StartMenu.menu)

    dp.register_message_handler(cost_effectiveness,
                                content_types=['text'],
                                text='Рентабельность',
                                state=StartMenu.menu)
