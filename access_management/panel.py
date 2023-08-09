from aiogram import Dispatcher, types
from common.states.access_states import *
from common.comands import access_management_menu


async def back_to_access_management_panel(message: types.Message):
    await PanelAccessManagement.menu.set()
    await message.answer('Действие отменено', reply_markup=types.ReplyKeyboardRemove())
    return await access_management_menu(message)


def register_handlers_access_management_panel(dp: Dispatcher):
    dp.register_message_handler(back_to_access_management_panel,
                                content_types=['text'],
                                text='↩️ Отменить и вернуться в панель управления',
                                state=[FormAddNewUser.id, FormAddNewUser.name,
                                       FormRemoveUser.id, FormRemoveUser.check])
