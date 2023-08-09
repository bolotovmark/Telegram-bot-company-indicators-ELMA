from aiogram.dispatcher.filters.state import State, StatesGroup


class StartMenu(StatesGroup):
    menu = State()


class PanelAccessManagement(StatesGroup):
    menu = State()


#  PanelAccessManagement
class FormAddNewUser(StatesGroup):
    id = State()
    name = State()


#  PanelAccessManagement
class FormRemoveUser(StatesGroup):
    id = State()
    check = State()
