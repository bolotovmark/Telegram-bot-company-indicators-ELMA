from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from elma.elma import elma_get_list_indicators


async def dynamic_kb_company_indicators(offset):
    company_indicators = await elma_get_list_indicators()

    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    if company_indicators:
        offset_list = company_indicators[offset:][:5]
        for row in offset_list:
            inline_kb_full.add(InlineKeyboardButton(f"{row}", callback_data=f"{row}"))

        if offset >= 5:
            if len(offset_list) != 5:
                inline_kb_full.add(InlineKeyboardButton("⏪Назад", callback_data="back"))
            else:
                inline_kb_full.row(InlineKeyboardButton("⏪Назад", callback_data="back"),
                                   InlineKeyboardButton("⏩Вперед", callback_data="next"))
        else:
            inline_kb_full.add(InlineKeyboardButton("⏩Вперед", callback_data="next"))

    else:
        inline_kb_full.add(InlineKeyboardButton("⏪Назад", callback_data="back"))

    return inline_kb_full
