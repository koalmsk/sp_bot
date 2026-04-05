from utils import util_funcs
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import types, Router
from aiogram import filters
from states.states import Admin_states
from utils import bot_text
from utils import config
from keyboards import admin_keyboards


admin_handler_route = Router()


@admin_handler_route.message(
    filters.Command("admin"), F.chat.func(lambda chat: util_funcs.check_admin(chat.id))
)
async def admin_start_cmd(message: types.Message, state: FSMContext):
    print(message.chat.id)
    print(util_funcs.check_admin(message.chat.id))
    await message.answer(
        text=bot_text.ADMIN_PANEL,
        reply_markup=admin_keyboards.edit_config_keyboard(**config.get_data()),
    )
    await state.set_state(Admin_states.Edit_panel)


@admin_handler_route.message(StateFilter(Admin_states.Value_for_config))
async def edit_config_handler(message: types.Message, state: FSMContext):
    try:
        value = float(message.text)
        param = await state.get_data()

        config.edit_config(place=param["Edit_panel"], value=value)
        await message.answer(
            text=bot_text.CONFIG_EDITED,
            reply_markup=admin_keyboards.edit_config_keyboard(**config.get_data()),
        )
        await state.set_state(Admin_states.Edit_panel)
    except:
        await message.answer(text=bot_text.ERROR_INPUT[1])
        await state.clear()
