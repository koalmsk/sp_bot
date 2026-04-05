from aiogram.filters import StateFilter
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F
from aiogram import filters
from states.states import User_states
from utils import bot_text, util_funcs, config, google_sheets
import json

from keyboards.user_keyboards import (
    user_start_keyboard,
    create_reply_keyboard,
    error_link_keyboard,
    to_start_keyboard,
)

user_handler_route = Router()


@user_handler_route.message(filters.Command("start"))
async def start_cmd(message: types.Message, state: FSMContext):
    await state.set_state(User_states.Start_state)
    await message.answer(text=bot_text.HELLO, reply_markup=user_start_keyboard)
    print(message.from_user.username)


@user_handler_route.message(StateFilter(User_states.Start_state), F.text.isdigit())
async def forever_calc(message: types.Message, state: FSMContext):
    china_price = abs(int(message.text))
    answer = bot_text.PRICE.format(
        price=util_funcs.calculate_price(
            price_china=china_price, data=config.get_data()
        )
    )
    await message.answer(text=answer, reply_markup=to_start_keyboard)

    await state.set_state(User_states.Start_state)


@user_handler_route.message(StateFilter(User_states.Calc))
async def send_calculate(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        china_price = abs(int(message.text))
        answer = bot_text.PRICE.format(
            price=util_funcs.calculate_price(
                price_china=china_price, data=config.get_data()
            ),
            reply_markup=to_start_keyboard,
        )
        await message.answer(text=answer, reply_markup=to_start_keyboard)
    else:
        await message.answer(text=bot_text.ERROR_INPUT[0])

    await state.set_state(User_states.Start_state)


@user_handler_route.message(StateFilter(User_states.let_me_link))
async def let_me_link_cmd(message: types.Message, state: FSMContext):

    if message.text == bot_text.ACCEPT_ORDER_BUTTONS[1]:
        await message.answer(
            bot_text.ORDER_IS_STOPED, reply_markup=ReplyKeyboardRemove()
        )
        await message.answer(text=bot_text.HELLO, reply_markup=user_start_keyboard)
        await state.set_state(User_states.Start_state)
    else:
        link = message.text
        try:
            txt = bot_text.edit_product(link)
            await state.update_data(let_me_link=txt[0], let_me_name=txt[1])
            await message.answer(text=bot_text.LET_ME_PRICE)
            await state.set_state(User_states.let_me_price)

        except:
            await message.answer(
                text=bot_text.LINK_ERROR, reply_markup=error_link_keyboard
            )
            await message.answer(text=bot_text.MAKE_ORDER)


@user_handler_route.message(StateFilter(User_states.let_me_price))
async def let_me_price(message: types.Message, state: FSMContext):
    if message.text == bot_text.ACCEPT_ORDER_BUTTONS[1]:
        await message.answer(
            bot_text.ORDER_IS_STOPED, reply_markup=ReplyKeyboardRemove()
        )
        await message.answer(text=bot_text.HELLO, reply_markup=user_start_keyboard)
        await state.set_state(User_states.Start_state)
    else:
        try:
            price = int(message.text)
            await state.update_data(
                let_me_price_rub=util_funcs.calculate_price(price, config.get_data())
            )
            await state.update_data(let_me_price_ya=int(message.text))

            await message.answer(text=bot_text.LET_ME_SIZE)
            await state.set_state(User_states.let_me_size)
        except:
            await message.answer(text="Ошибка ввода, попробуйте ещё раз.")
            await message.answer(text=bot_text.LET_ME_PRICE)


@user_handler_route.message(StateFilter(User_states.let_me_size))
async def let_me_size(message: types.Message, state: FSMContext):
    if message.text == bot_text.ACCEPT_ORDER_BUTTONS[1]:
        await message.answer(
            bot_text.ORDER_IS_STOPED, reply_markup=ReplyKeyboardRemove()
        )
        await message.answer(text=bot_text.HELLO, reply_markup=user_start_keyboard)
        await state.set_state(User_states.Start_state)
    else:
        size = message.text

        await state.update_data(let_me_size=size)

        await message.answer(
            text=bot_text.DELIVER_TEXT,
            reply_markup=create_reply_keyboard(*bot_text.DELIVER_BUTTONS),
            parse_mode="Markdown",
        )
        await state.set_state(User_states.let_me_delivery)


@user_handler_route.message(StateFilter(User_states.let_me_delivery))
async def let_me_deliver(message: types.Message, state: FSMContext):
    if message.text in bot_text.DELIVER_BUTTONS:
        if message.text == bot_text.ACCEPT_ORDER_BUTTONS[1]:
            await message.answer(
                bot_text.ORDER_IS_STOPED, reply_markup=ReplyKeyboardRemove()
            )
            await message.answer(text=bot_text.HELLO, reply_markup=user_start_keyboard)
            await state.set_state(User_states.Start_state)
        else:
            deliver = message.text

            await state.update_data(let_me_delivery=deliver)
            order_data = await state.get_data()
            print(order_data)
            await message.answer(
                text=bot_text.ready_order(**order_data),
                reply_markup=create_reply_keyboard(*bot_text.ACCEPT_ORDER_BUTTONS),
                parse_mode="Markdown",
            )
            await state.set_state(User_states.accept_order)
    else:
        await message.answer(
            text=bot_text.DELIVER_TEXT,
            reply_markup=create_reply_keyboard(*bot_text.DELIVER_BUTTONS),
            parse_mode="Markdown",
        )


@user_handler_route.message(StateFilter(User_states.accept_order))
async def accept_order(message: types.Message, state: FSMContext):
    if message.text in bot_text.ACCEPT_ORDER_BUTTONS:
        if message.text == bot_text.ACCEPT_ORDER_BUTTONS[1]:
            await message.answer(
                bot_text.ORDER_IS_STOPED, reply_markup=ReplyKeyboardRemove()
            )
            await message.answer(text=bot_text.HELLO, reply_markup=user_start_keyboard)
        elif message.text == bot_text.ACCEPT_ORDER_BUTTONS[0]:
            data = await state.get_data()
            print(data)  # все данные заказа которые нужно передавать
            await message.answer(
                "Подождите, обработка", reply_markup=ReplyKeyboardRemove()
            )
            sheet = google_sheets.googleSheet()
            order_code = sheet.add_order(
                str(message.from_user.id),
                f"https://t.me/{message.from_user.username}",
                data["let_me_link"],
                data["let_me_name"],
                data["let_me_size"],
                data["let_me_price_ya"],
                json.load(open("src/utils/config.json"))["config"]["currency"],
                data["let_me_price_rub"],
                bot_text.DELIVER_TABLE[data["let_me_delivery"]],
            )
            await message.answer(
                text=bot_text.ACCEPTED_ORDER.format(order_id=order_code),
                parse_mode="Markdown",
                reply_markup=to_start_keyboard,
            )
            await util_funcs.notification_to_admin(
                text = bot_text.NOTIFICATION_TEXT.format(user=message.from_user.username)
                )

        await state.set_state(User_states.Start_state)
    else:
        await message.answer(
            text="Ошибка, попробуйте еще раз.",
            reply_markup=create_reply_keyboard(*bot_text.ACCEPT_ORDER_BUTTONS),
            parse_mode="Markdown",
        )


@user_handler_route.message(StateFilter(User_states.monitor_order))
async def monitor_order_handler(message: types.Message, state: FSMContext):
    order_id = message.text
    await message.answer("Подождите, обработка.")
    if str(message.from_user.id) in order_id:

        sheet = google_sheets.googleSheet()
        try:
            order_data = sheet.get_order(order_id)
            await message.answer(
                text=bot_text.monitor_order_text(**order_data),
                parse_mode="Markdown",
                reply_markup=to_start_keyboard,
            )
        except:
            await message.answer(
                text=bot_text.ERROR_MONITOR_ORDER, reply_markup=to_start_keyboard
            )
    else:
        await message.answer(
            text=bot_text.ERROR_MONITOR_ORDER, reply_markup=to_start_keyboard
        )

    await state.set_state(User_states.Start_state)
