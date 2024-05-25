from aiogram.fsm.state import State, StatesGroup


class AddingEmailStatesGroup(StatesGroup):
    CHECK_OUT = State()
    FOLDER_SELECTION = State()


class FolderStatesGroup(StatesGroup):
    FOLDER_SELECTION = State()
    FOLDER = State()
    FOLDER_DELETION = State()
    FOLDER_CREATION = State()
    EMAIL_LIST = State()    
    EMAIL = State()
    EMAIL_ADDITION = State()
