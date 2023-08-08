from aiogram.dispatcher.filters.state import State, StatesGroup


class StartMenu(StatesGroup):
    menu = State()


class PanelAccessManagement(StatesGroup):
    menu = State()