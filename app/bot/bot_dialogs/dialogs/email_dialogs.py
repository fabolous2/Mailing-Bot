from aiogram import F

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import (
    ScrollingGroup,
    Select,
    Row,
    PrevPage,
    NextPage,
    CurrentPage,
    Back,
    Button,
    Start
)
from aiogram_dialog.widgets.input import TextInput

from app.bot.bot_dialogs.callbacks.email_callbacks import on_cancel_adding, on_confirm_adding, on_select_folder_for_adding
from app.bot.states import FolderStatesGroup, AddingEmailStatesGroup
from app.bot.bot_dialogs.getters import folders_getter, emails_getter, get_one_email
from app.bot.bot_dialogs.callbacks import (
    selected_folder,
    deletion_check_out,
    delete_folder,
    cancel_folder_deletion_handler,
    add_folder_handler,
    on_input_folder_name,
    selected_email_handler,
    email_deletion_handler,
    switch_to_email_list,
    email_addition_handler,
    on_input_emails
)


async def close_dialog(_, __, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.done()


email_main_dialog = Dialog(
    Window(
        Const('You don\'t have any folders.', when=F['is_empty'] == 1),
        Const('Select a folder', when=F['is_empty'] == 0),
        ScrollingGroup(
            Select(
                id="folder_select",
                items="folders",
                item_id_getter=lambda item: item.folder_id,
                text=Format("📁 {item.name}"),
                on_click=selected_folder,
            ),
            id="folder_group",
            height=10,
            width=1,
            hide_on_single_page=True,
            hide_pager=True,
            when=F['is_empty'] == 0
        ),
        Button(
            text=Format('➕ Add folder'),
            id='folder_addition',
            on_click=add_folder_handler,
        ),
        state=FolderStatesGroup.FOLDER_SELECTION,
    ),
    Window(
        Const(text='📂:'),
        Button(
            text=Format('🗞️ Email List'),
            id='email_list',
            on_click=switch_to_email_list
        ),
        Button(
            text=Format('💾 Add'),
            on_click=email_addition_handler,
            id='email_addition'
        ),
        Button(
            text=Format('🗑️ Delete Folder'),
            on_click=deletion_check_out,
            id='folder_deletion'
        ),
        Back(Format('◀️')),
        state=FolderStatesGroup.FOLDER
    ),
    Window(
        Const('📃:', when=F['is_empty'] == 0),
        Const('🕳️Empty (', when=F['is_empty'] == 1),
        ScrollingGroup(
            Select(
                id="email_select",
                items="emails",
                item_id_getter=lambda item: item.email,
                text=Format("📧 {item.email}"),
                on_click=selected_email_handler
            ),
            id="email_group",
            height=10,
            width=2,
            hide_on_single_page=True,
            hide_pager=True,
            when=F['is_empty'] == 0
        ),
        Row(
            PrevPage(
                scroll="email_group", text=Format("◀️"),
            ),
            CurrentPage(
                scroll="email_group", text=Format("{current_page1}"),
            ),
            NextPage(
                scroll="email_group", text=Format("▶️"),
            ),
            when=F['is_empty'] == 0
        ),
        Back(
            text=Format('◀️ Back'),
            # on_click=back_to_folder,
        ),
        state=FolderStatesGroup.EMAIL_LIST,
        getter=emails_getter,
    ),
    Window(
        Format('ℹ️\n• <b>Email:</b> {email.email}\n• <b>Sendments:</b> {email.sendments}'),
        Button(
        text=Const('🗑️ Delete'),
        id='email_deletion',
        on_click=email_deletion_handler,
        ),
        Back(Format('◀️ Back')),
        state=FolderStatesGroup.EMAIL,
        getter=get_one_email
    ),
    Window(
        Const('Type an emails and separate them by comma or whitespace'),
        TextInput(
            id='email_input',
            on_success=on_input_emails
        ),
        state=FolderStatesGroup.EMAIL_ADDITION,
    ),
    Window(
        Const('Name of your folder:'),
        TextInput(
            on_success=on_input_folder_name,
            id='folder_name'
        ),
        state=FolderStatesGroup.FOLDER_CREATION,
    ),
    Window(
        Const('⚠️ Are you sure?'),
        Row(
            Button(
                Format('Delete'),
                id='deletion',
                on_click=delete_folder,
            ),
            Button(
                Format('Cancel ❌'),
                id='cancel_deletion',
                on_click=cancel_folder_deletion_handler
            )
        ),
        state=FolderStatesGroup.FOLDER_DELETION
    ),
    getter=folders_getter,
)

email_adding_dialog = Dialog(
    Window(
        Const(text='Do u want to add it to ur email list 📃?'),
        Row(
            Button(
                text=Const(text='❌ NO'),
                id='cancel_button',
                on_click=on_cancel_adding
            ),
            Button(
                text=Const(text='✅ Yeah'),
                id='confirm_button',
                on_click=on_confirm_adding
            ),
        ),
        state=AddingEmailStatesGroup.CHECK_OUT,
    ),
    Window(
        Const('Выберите папку, в которую хотите добавить почты:', when=F['is_empty'] == 0),
        ScrollingGroup(
            Select(
                id="folder_select",
                items="folders",
                item_id_getter=lambda item: item.folder_id,
                text=Format("📁 {item.name}"),
                on_click=on_select_folder_for_adding,
            ),
            id="folder_group",
            height=10,
            width=1,
            hide_on_single_page=True,
            hide_pager=True,
            when=F['is_empty'] == 0
        ),
        state=AddingEmailStatesGroup.FOLDER_SELECTION,
        getter=folders_getter,
    ),
    Window(
        Const('🎉 successfully added'),
        Start(
            text=Const('🗞️ Email List'),
            state=FolderStatesGroup.FOLDER_SELECTION,
            id='look_up_list'
        ),
        state=AddingEmailStatesGroup.SUCCESS
    ),
    on_process_result=close_dialog
)