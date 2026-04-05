from aiogram.fsm.state import State, StatesGroup


class User_states(StatesGroup):
    Start_state = State()
    Calc = State()
    let_me_link = State()
    let_me_price = State()
    let_me_size = State()
    let_me_delivery = State()
    accept_order = State()
    monitor_order = State()


class Admin_states(StatesGroup):
    Edit_panel = State()
    Value_for_config = State()
