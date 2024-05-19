from aiogram.fsm.state import State, StatesGroup


class RegisterStatesGroup(StatesGroup):
    EMAIL = State()
    PASSWORD = State()