from aiogram import F

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import (
    Const,
    Format,
    Jinja
)
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import (
    ScrollingGroup,
    Select,
    Button,
    Row,
    Calendar
)

from app.bot.bot_dialogs.callbacks import mailing_callbacks
from app.bot.states import MailingStatesGroup
from app.bot.bot_dialogs.getters import email_getter, mailing_getter


mailing_dialog = Dialog(
    Window(
        Const('You don\'t have any folders.', when=F['is_empty'] == 1),
        Const('Select a folder', when=F['is_empty'] == 0),
        ScrollingGroup(
            Select(
                id="folder_select",
                items="folders",
                item_id_getter=lambda item: item.folder_id,
                text=Format("📁 {item.name}"),
                on_click=mailing_callbacks.selected_folder,
            ),
            id="folder_group",
            height=10,
            width=1,
            hide_on_single_page=True,
            hide_pager=True,
            when=F['is_empty'] == 0
        ),
        state=MailingStatesGroup.FOLDER_SELECTION,
        getter=email_getter.folders_getter
    ),
    Window(
        Jinja(
'''
<b>Вот так выглядит ваше письмо:</b>

💼 <b>Subject:</b> <blockquote>{{settings.subject}}</blockquote>
💬 <b>Message:</b> <blockquote>{{settings.text}}</blockquote>
📥 <b>Recipements:</b> 📁 {{folder.name}}
'''
        ),
        Row(
            Button(
                text=Const('❌ Cancel'),
                id='cancel_mailing',
                on_click=mailing_callbacks.cancel_mailing_handler
            ),
            Button(
                text=Const('✅ Send Now'),
                id='confirm_mailing',
                on_click=mailing_callbacks.mailing_handler
            ),
        ),
        Button(
            text=Const('⏳ Schedule'),
            id='schedule_mailing',
            on_click=mailing_callbacks.schedule_mailing_handler
        ),
        state=MailingStatesGroup.MAILING,
        getter=mailing_getter.mail_getter,
    ),
    Window(
        Const('Выберите дату отправки: '),
        Calendar(
            id='calendar',
            on_click=mailing_callbacks.on_date_selected
        ),
        state=MailingStatesGroup.SCHEDULER,
    ),
    Window(
        Const('Напишите время отправки (xx:xx): '),
        TextInput(
            id='time_input',
            on_success=mailing_callbacks.on_input_time
        ),
        state=MailingStatesGroup.TIME,
    ),
    Window(
        Format('Вы уверены что хотите запустить рассылку {date} в {time}?'),
        Row(
            Button(
                text=Const('❌ Cancel'),
                id='cancel_sceduling',
                on_click=mailing_callbacks.cancel_scheduling
            ),
            Button(
                text=Const('✅ Yes'),
                id='confirm_scheduling',
                on_click=mailing_callbacks.confirm_scheduling
            ),
        ),
        state=MailingStatesGroup.SCHEDULE_MAILING,
        getter=mailing_getter.scheduled_time_getter,
    )
)