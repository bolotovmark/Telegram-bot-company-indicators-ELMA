from aiogram.dispatcher.filters.state import State, StatesGroup


class StartMenu(StatesGroup):
    menu = State()


class PanelAccessManagement(StatesGroup):
    menu = State()


#  PanelAccessManagement
class FormAddNewUser(StatesGroup):
    id = State()
    position_name = State()
    name = State()
    position_id = 0


#  PanelAccessManagement
class FormRemoveUser(StatesGroup):
    id = State()
    check = State()
