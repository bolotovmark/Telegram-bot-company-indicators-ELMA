from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

###
start_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
start_menu.add(types.InlineKeyboardButton(text="Выручка"))
start_menu.add(types.InlineKeyboardButton(text="План поступления"))
start_menu.add(types.InlineKeyboardButton(text="Рентабельность"))
###