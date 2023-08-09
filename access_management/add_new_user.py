from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from common.states.access_states import FormAddNewUser, PanelAccessManagement
from db.methods import db_exists_user, db_insert_new_user
from common.comands import access_management_menu
from common.keyboards.static import kb_empty_method


# @dp.message_handler(content_types=['text'], text='Добавить', state=FormChangeListUsers.menu)
async def start_form_AddNewUser(message: types.Message):
    await FormAddNewUser.id.set()
    await message.answer("Введите ID нового пользователя:", reply_markup=kb_empty_method)


# @dp.message_handler(lambda message: not message.text.isdigit(), state=FormAddNewUser.id)
async def process_id_invalid(message: types.Message):
    """
    id is invalid
    """
    return await message.reply("ID должен состоять только из чисел. Пожалуйста, уточните ID у нового пользователя.")


# @dp.message_handler(lambda message: message.text.isdigit(), state=FormAddNewUser.id)
async def process_id(message: types.Message, state: FSMContext):
    user = await db_exists_user(int(message.text))
    if not user:
        await FormAddNewUser.next()
        await state.update_data(id=int(message.text))

        await message.answer("Напишите ФИО", reply_markup=kb_empty_method)
    else:
        await message.answer(f"Этот пользователь уже находиться в базе")


# @dp.message_handler(state=FormAddNewUser.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        await message.answer(f"Новый пользователь добавлен:\n"
                             f"ID: {data['id']}\n"
                             f"ФИО: {data['name']}")
    await state.finish()
    await db_insert_new_user(data['id'], data['name'])
    await PanelAccessManagement.menu.set()

    return await access_management_menu(message)


def register_handlers_access_management_add_new_user(dp: Dispatcher):
    dp.register_message_handler(start_form_AddNewUser, content_types=['text'],
                                text='Добавить',
                                state=PanelAccessManagement.menu)
    dp.register_message_handler(process_id_invalid,
                                lambda message: not message.text.isdigit()
                                                and message.text != "↩️ Отменить и вернуться в панель управления",
                                state=FormAddNewUser.id)
    dp.register_message_handler(process_id,
                                lambda message: message.text.isdigit()
                                                and message.text != "↩️ Отменить и вернуться в панель управления",
                                state=FormAddNewUser.id)
    dp.register_message_handler(process_name,
                                lambda message: message.text != "↩️ Отменить и вернуться в панель управления",
                                state=FormAddNewUser.name)
