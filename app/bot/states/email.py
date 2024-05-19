from aiogram.fsm.state import State, StatesGroup


class AddingEmailStatesGroup(StatesGroup):
    EMAIL_INPUT = State()
    EMAIL = State()


class EmailListSG(StatesGroup):
    FOLDER = State()
    EMAIL_LIST = State()
    EMAIL = State()