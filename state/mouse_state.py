from aiogram.dispatcher.filters.state import State, StatesGroup


class MouseState(StatesGroup):
    action = State()
