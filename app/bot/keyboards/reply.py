from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu_kb_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📨 Mailing')
        ],
        [
            KeyboardButton(text='📪 Emails'),
            KeyboardButton(text='⚙️ Settings')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
)