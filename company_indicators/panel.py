from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from common.states.company_indicators import PanelCompanyIndicators
from common.keyboards.dynamic import dynamic_kb_company_indicators
from common.keyboards.static import kb_empty_method


async def start_form_select_company_indicator(message: types.Message):
    await PanelCompanyIndicators.select_indicators.set()
    await message.answer("Открыта форма просмотра показателей компании",
                         reply_markup=kb_empty_method)

    await message.answer("Выберите интересующий показатель",
                         reply_markup=await dynamic_kb_company_indicators(0))

