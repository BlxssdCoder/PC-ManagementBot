from aiogram.dispatcher.filters.state import State, StatesGroup


class ManagementState(StatesGroup):
    action = State()
    cmd = State()
