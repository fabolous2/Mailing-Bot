from aiogram import F

from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import (
    ScrollingGroup,
    Select,
    Button,
    Start,
    Back
)
from aiogram_dialog.widgets.input import TextInput

from app.bot.bot_dialogs.getters.email_getter import folders_getter
from app.bot.states import SettingsStatesGroup, FolderStatesGroup
from app.bot.bot_dialogs.callbacks import settings
from app.bot.bot_dialogs.getters import settings_getter



async def close_dialog(_, __, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.done()


settings_main_dialog = Dialog(
    Window(
        Const('You don\'t have any folders.', when=F['is_empty'] == 1),
        Const('Select a folder', when=F['is_empty'] == 0),
        ScrollingGroup(
            Select(
                id="folder_select",
                items="folders",
                item_id_getter=lambda item: item.folder_id,
                text=Format("📁 {item.name}"),
                on_click=settings.selected_folder,
            ),
            id="folder_group",
            height=10,
            width=1,
            hide_on_single_page=True,
            hide_pager=True,
            when=F['is_empty'] == 0
        ),
        Start(
            text=Const('➕ Add folder'),
            id='folder_addition',
            state=FolderStatesGroup.FOLDER_CREATION,
        ),
        state=SettingsStatesGroup.FOLDER_SELECTION,
        getter=folders_getter,
    ),
    Window(
        Format(
'''
✉️ Вот так выглядит ваше письмо:\n\n
💼 Subject: <blockquote>{settings.subject}</blockquote>\n
💬 Message: <blockquote>{settings.text}</blockquote>
'''
        ),
        Button(
            text=Const('Edit Subject 🛠️'),
            id='edit_subject',
            on_click=settings.switch_to_subject_input
        ),
        Button(
            text=Const('Edit Message 🛠️'),
            id='edit_message',
            on_click=settings.switch_to_message_input,
        ),
        Back(Const('◀️ Back')),
        getter=settings_getter.user_settings_getter,
        state=SettingsStatesGroup.MAIN_MENU
    ),
    Window(
        Const('💼 Type a new subject:'),
        TextInput(
            id='subject_input',
            on_success=settings.on_input_subject
        ),
        state=SettingsStatesGroup.SUBJECT_INPUT,
    ),
    Window(
        Const('💬 Type a new message:'),
        TextInput(
            id='message_input',
            on_success=settings.on_input_message
        ),
        state=SettingsStatesGroup.MESSAGE_INPUT,
    )
)
