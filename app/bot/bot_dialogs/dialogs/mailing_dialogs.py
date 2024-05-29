from aiogram import F

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import (
    Const,
    Format,
    Jinja
)
from aiogram_dialog.widgets.kbd import (
    ScrollingGroup,
    Select,
    Button,
    Row
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
                text=Const('✅ Send'),
                id='confirm_mailing',
                on_click=mailing_callbacks.mailing_handler
            ),
        ),
        state=MailingStatesGroup.MAILING,
        getter=mailing_getter.mail_getter,
    )
)