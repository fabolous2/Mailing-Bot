from aiogram.fsm.state import State, StatesGroup

class MailingStatesGroup(StatesGroup):
    AUDIOS = State()
    FOLDER_SELECTION = State()
    MAILING = State()