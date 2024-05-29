from aiogram.fsm.state import State, StatesGroup


class SettingsStatesGroup(StatesGroup):
    FOLDER_SELECTION = State()
    MAIN_MENU = State()
    SUBJECT_INPUT = State()
    MESSAGE_INPUT = State()

    