from itertools import groupby

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from common.states.company_indicators import PanelCompanyIndicators
from common.keyboards.dynamic import dynamic_kb_company_indicators
from common.keyboards.static import kb_back_to_main_panel
from elma.elma import elma_get_info_about_indicator


async def start_form_select_company_indicator(message: types.Message, state: FSMContext):
    await PanelCompanyIndicators.select_indicators.set()
    async with state.proxy() as data:
        data['page'] = 0

    await message.answer("Открыта форма просмотра показателей компании",
                         reply_markup=kb_back_to_main_panel)

    await message.answer("Выберите интересующий показатель",
                         reply_markup=await dynamic_kb_company_indicators(0))


async def select_company_indicators(callback_query: types.CallbackQuery, state: FSMContext):
    company_indicator: str
    page: int

    async with state.proxy() as data:
        data['company_indicator'] = callback_query.data
        company_indicator = data['company_indicator']
        page = data['page']

    info = await elma_get_info_about_indicator(company_indicator)
    output_text = f'📈  *{str(company_indicator).title()}*'

    for g in groupby(sorted(info, key=lambda x: x[0]), key=lambda x: x[0]):
        output_text += f"\n\n🔻_{g[0]}_\n"
        for h in groupby(sorted(g[1], key=lambda x: x[1]), key=lambda x: x[1]):
            for i in h[1]:
                if h[0] != '':
                    output_text += f"\n▪️{h[0]}: {i[2]}"
                else:
                    output_text += f"\n▪️{i[2]}"

    bot = callback_query.bot
    await bot.edit_message_text(
        text=output_text,
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=await dynamic_kb_company_indicators(page),
        parse_mode="Markdown"
    )


async def process_next_page(callback_query: types.CallbackQuery, state: FSMContext):
    page: int
    async with state.proxy() as data:
        data['page'] = int(data['page']) + 5
        page = data['page']

    bot = callback_query.bot
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=await dynamic_kb_company_indicators(page)
    )


async def process_back_page(callback_query: types.CallbackQuery, state: FSMContext):
    page: int
    async with state.proxy() as data:
        data['page'] = int(data['page']) - 5
        page = data['page']

    bot = callback_query.bot
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=await dynamic_kb_company_indicators(page)
    )


def register_handlers_select_company_indicators(dp: Dispatcher):
    dp.register_callback_query_handler(select_company_indicators,
                                       lambda c: c.data not in ['next', 'back'],
                                       state=PanelCompanyIndicators.select_indicators)

    dp.register_callback_query_handler(process_next_page,
                                       lambda c: c.data == "next",
                                       state=PanelCompanyIndicators.select_indicators)

    dp.register_callback_query_handler(process_back_page,
                                       lambda c: c.data == "back",
                                       state=PanelCompanyIndicators.select_indicators)
