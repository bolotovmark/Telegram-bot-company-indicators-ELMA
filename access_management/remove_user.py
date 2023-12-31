from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from common.states.access_states import PanelAccessManagement, FormRemoveUser

from db.methods import db_exists_user
from common.keyboards.static import kb_empty_method, kb_boolean_keyboard
from common.comands import access_management_menu


# @dp.message_handler(content_types=['text'], text='Удалить', state=FormChangeListUsers.menu)
async def remove_user(message: types.Message):
    await FormRemoveUser.id.set()
    await message.answer("Введите ID пользователя, которого хотите удалить из базы",
                         reply_markup=kb_empty_method)


# @dp.message_handler(lambda message: not message.text.isdigit(), state=FormRemoveUser.id)
async def process_remove_id_invalid(message: types.Message):
    """
    id is invalid
    """
    return await message.reply("ID должен состоять только из чисел. Попробуйте ввести заново",
                               reply_markup=kb_empty_method)


# @dp.message_handler(lambda message: message.text.isdigit(), state=FormRemoveUser.id)
async def process_remove_id(message: types.Message, state: FSMContext):
    user = await db_exists_user(message.text)
    if user:
        async with state.proxy() as data:
            data['id'] = message.text
            await FormRemoveUser.check.set()
            await message.answer(f"*{user[1]}*\n"
                                 f"ID: {user[0]}\n\n"
                                 f"⚠️\n"
                                 f"*Удалить этого пользователя из базы?*", parse_mode="MarkdownV2",
                                 reply_markup=kb_boolean_keyboard)
    else:
        await message.reply(f"Этого пользователя не существует в базе данных. Попробуйте ввести заново",
                            reply_markup=kb_empty_method)


# @dp.message_handler(content_types=['text'], text='❌', state=FormRemoveUser.check)
async def remove_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await PanelAccessManagement.menu.set()
    await message.answer("Операция отменена")
    return await access_management_menu(message)


def register_handlers_access_management_remove_user(dp: Dispatcher):
    dp.register_message_handler(remove_user,
                                content_types=['text'],
                                text='Удалить',
                                state=PanelAccessManagement.menu)

    dp.register_message_handler(process_remove_id_invalid,
                                lambda message: not message.text.isdigit()
                                                and message.text != "↩️ Отменить и вернуться в панель управления",
                                state=FormRemoveUser.id)

    dp.register_message_handler(process_remove_id,
                                lambda message: message.text.isdigit()
                                                and message.text != "↩️ Отменить и вернуться в панель управления",
                                state=FormRemoveUser.id)

    dp.register_message_handler(remove_cancel,
                                content_types=['text'],
                                text='❌',
                                state=FormRemoveUser.check)
