from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from common.states.company_indicators import PanelCompanyIndicators
from common.states.none_auth import NoneAuth
from common.states.access_states import StartMenu, PanelAccessManagement
from company_indicators.panel import start_form_select_company_indicator
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


async def start_menu(message: types.Message):
    await message.answer("Для навигации используйте панель", reply_markup=kb_start_menu)


async def access_management_menu(message: types.Message):
    await PanelAccessManagement.menu.set()
    await message.answer("Панель управления доступом", reply_markup=kb_access_management_menu)


async def cancel_access_management_menu(message: types.Message):
    await StartMenu.menu.set()
    return await start_menu(message)


async def select_company_indicator(message: types.Message, state: FSMContext):
    await PanelCompanyIndicators.select_indicators.set()
    return await start_form_select_company_indicator(message, state)


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
                                state=[PanelAccessManagement, PanelCompanyIndicators])

    dp.register_message_handler(select_company_indicator,
                                content_types=['text'],
                                text='📊 Показатели',
                                state=StartMenu.menu)
