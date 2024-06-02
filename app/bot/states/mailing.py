from aiogram.fsm.state import State, StatesGroup

class MailingStatesGroup(StatesGroup):
    AUDIOS = State()
    FOLDER_SELECTION = State()
    MAILING = State()
    SCHEDULER = State()
    TIME = State()
    SCHEDULE_MAILING = State()


class ScheduledMailingSG(StatesGroup):
    MAILING_SELECTION = State()
    MAILING_INFO = State()
