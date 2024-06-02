from aiogram import F

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import (
    Const,
    Format,
)
from aiogram_dialog.widgets.kbd import (
    ScrollingGroup,
    Select,
    Button,
    Back
)

from app.bot.bot_dialogs.callbacks import mailing_callbacks
from app.bot.states import ScheduledMailingSG
from app.bot.bot_dialogs.getters import mailing_getter


scheduled_mailings_dialog = Dialog(
    Window(
        Const('Select a scheduled mailing', when=F['is_empty'] == 0),
        Const('Empty', when=F['is_empty'] == 1),
        ScrollingGroup(
            Select(
                id="mailing_selection",
                items="mailings",
                item_id_getter=lambda item: item.job_id,
                text=Format("📬 {item.scheduled_time}"),
                on_click=mailing_callbacks.selected_mailing,
            ),
            id="folder_group",
            height=10,
            width=1,
            hide_on_single_page=True,
            hide_pager=True,
            when=F['is_empty'] == 0
        ),
        state=ScheduledMailingSG.MAILING_SELECTION,
        getter=mailing_getter.scheduled_mailings_getter
    ),
    Window(
        Format(
'''
📁 <b>Folder</b>: {folder_name}
⌚ <b>Time</b>: {mailing.scheduled_time}
'''
        ),
        Button(
            Const('❌ Отменить отправку'),
            id='cancel_mailing',
            on_click=mailing_callbacks.cancel_sheduled_mailing_task
        ),
        Back(Const('◀️ Back')),
        state=ScheduledMailingSG.MAILING_INFO,
        getter=mailing_getter.mailings_info_getter
    )
)
