from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


error_link_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Как заказать", url="https://telegra.ph/Vsyo-o-Poizon-02-28-2"
            )
        ]
    ]
)

user_start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Калькулятор💴", callback_data="calculate"),
            InlineKeyboardButton(text="Оформить заказ🧾", callback_data="make_order"),
        ],
        [
            InlineKeyboardButton(text="Отзывы📖", url="https://t.me/SPstorehere/4"),
            InlineKeyboardButton(text="SP Store ", url="https://t.me/SPstorehere"),
        ],
        [
            InlineKeyboardButton(
                text="Отследить заказ📆", callback_data="monitor_order"
            ),
            InlineKeyboardButton(
                text="Как заказать❓", url="https://telegra.ph/Vsyo-o-Poizon-02-28-2"
            ),
        ],
        [
            InlineKeyboardButton(
                    text="SPCOIN", url="https://t.me/blum/app?startapp=memepadjetton_SPCOIN_QGK6N-ref_eJe7EdtVGT"
                ),
        ]
    ]
)
cancel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Отмена", callback_data="cancel")]]
)


to_start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="На главную", callback_data="to_start")]
    ]
)


def create_reply_keyboard(*buttons):

    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[[KeyboardButton(text=button) for button in buttons]],
    )
