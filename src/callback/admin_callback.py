from keyboards import admin_keyboards
from aiogram import types
from aiogram import Router
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from states.states import Admin_states
from utils.config import reset_config, get_data
from utils import bot_text


admin_callback_router = Router()


@admin_callback_router.callback_query(
    StateFilter(Admin_states.Edit_panel), F.data.startswith("ad_")
)
async def edit_config_clbck(callback: types.CallbackQuery, state: FSMContext):
    callback_data = callback.data.replace("ad_", "")
    if callback_data == "reset":
        reset_config()
        await callback.answer(text=bot_text.CONFIG_RESET)
        await callback.message.edit_reply_markup(
            inline_message_id=callback.inline_message_id,
            reply_markup=admin_keyboards.edit_config_keyboard(**get_data()),
        )
    else:
        parametr = callback_data.split("-")
        await state.update_data(Edit_panel=parametr)
        await callback.answer(text=bot_text.CONFIG_EDITED)
        await callback.message.answer(
            text=bot_text.LET_ME_VALUE.format(
                param=str(parametr).strip("[',']").replace("-", " ")
            ),
            reply_markup=admin_keyboards.cancel_keyboard,
        )
        await state.set_state(Admin_states.Value_for_config)


@admin_callback_router.callback_query(StateFilter(Admin_states.Value_for_config))
async def edit_config_clbck(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "cancel":
        await callback.message.delete()
        await callback.answer("Отмена")
    await state.set_state(Admin_states.Edit_panel)
