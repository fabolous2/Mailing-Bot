from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu_kb_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📨 Mailing')
        ],
        [
            KeyboardButton(text='📪 Emails'),
            KeyboardButton(text='🎶 Beats'),
        ],
        [
            KeyboardButton(text='⚙️ Settings')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
)