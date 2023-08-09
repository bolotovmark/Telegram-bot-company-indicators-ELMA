from aiogram.dispatcher.filters.state import State, StatesGroup


class PanelCompanyIndicators(StatesGroup):
    select_indicators = State()
