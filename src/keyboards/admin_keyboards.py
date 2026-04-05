from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def edit_config_keyboard(currency, percentage, up, down):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"курс ({currency})", callback_data=f"ad_currency"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"процент ({percentage})", callback_data=f"ad_percentage"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"нижний порог ({down['limit']})",
                    callback_data=f"ad_down-limit",
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"нижний навар ({down['profit']})",
                    callback_data=f"ad_down-profit",
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"верхний порог ({up['limit']})", callback_data=f"ad_up-limit"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"верхний навар ({up['profit']})",
                    callback_data=f"ad_up-profit",
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"Сбросить изменения", callback_data=f"ad_reset"
                )
            ],
        ]
    )
    return keyboard


cancel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Отмена", callback_data="cancel")]]
)
