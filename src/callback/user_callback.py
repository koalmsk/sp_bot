from keyboards import user_keyboards
from aiogram import types
from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from states.states import User_states
from aiogram import types, Router, F

from keyboards.user_keyboards import (
    user_start_keyboard,
    create_reply_keyboard,
    cancel_keyboard,
)

from utils import bot_text

user_callback_router = Router()


@user_callback_router.callback_query(StateFilter(User_states.Start_state))
async def start_callbacks(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "calculate":
        await callback.message.answer(
            text=bot_text.LET_ME_PRICE, reply_markup=user_keyboards.cancel_keyboard
        )
        await callback.answer("Калькулятор")
        await state.set_state(User_states.Calc)

    if callback.data == "make_order":
        await callback.message.answer(
            text=bot_text.MAKE_ORDER,
            reply_markup=create_reply_keyboard(bot_text.ACCEPT_ORDER_BUTTONS[1]),
        )
        await callback.answer("Заказ")
        await state.set_state(User_states.let_me_link)

    if callback.data == "monitor_order":

        await callback.message.answer(
            text=bot_text.MONITOR_ORDER_START, reply_markup=cancel_keyboard
        )
        await callback.answer("Отслеживание заказа")
        await state.set_state(User_states.monitor_order)

    if callback.data == "to_start":
        await callback.message.answer(
            text=bot_text.HELLO, reply_markup=user_start_keyboard
        )
        await callback.answer("На главную")

        print(callback.message.from_user.username)


@user_callback_router.callback_query(
    StateFilter(User_states.Calc, User_states.monitor_order)
)
async def cancel_callbacks(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "cancel":
        await callback.message.delete()
        await callback.answer("Назад")
        await state.set_state(User_states.Start_state)
