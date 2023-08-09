from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

###
kb_start_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb_start_menu.add(types.InlineKeyboardButton(text="📊 Показатели"))
kb_start_menu.add(types.InlineKeyboardButton(text="🪪 Управление доступом"))
###

###
kb_access_management_menu = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="Добавить"),
            types.KeyboardButton(text="Удалить")
        ],
    ], resize_keyboard=True)
kb_access_management_menu.add(types.InlineKeyboardButton(text="Список пользователей"))
kb_access_management_menu.add(types.InlineKeyboardButton(text="↩️ Вернуться в главное меню"))
###

###
kb_empty_method = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb_empty_method.add(types.InlineKeyboardButton(text="↩️ Отменить и вернуться в панель управления"))
###

###
kb_boolean_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="✅"),
            types.KeyboardButton(text="❌")
        ],
    ], resize_keyboard=True)
kb_boolean_keyboard.add(types.InlineKeyboardButton(text="↩️ Отменить и вернуться в панель управления"))
###

###
kb_back_to_main_panel = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb_back_to_main_panel .add(types.InlineKeyboardButton(text="↩️ Вернуться в главное меню"))