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
    Button
)
from aiogram_dialog.widgets.input import TextInput


from app.bot.states import FolderStatesGroup
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
    back_to_folder,
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
    Window(
        Const('📃:', when=F['is_empty'] == 0),
        Const('🕳️Empty (', when=F['is_empty'] == 1),
        ScrollingGroup(
            Select(
                id="email_select",
                items="emails",
                item_id_getter=lambda item: item.email,
                text=Format("📧 {item.email}"),
                on_click=selected_email_handler,
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
            text=Format('◀️'),
            on_click=back_to_folder,
        ),
        state=FolderStatesGroup.EMAIL_LIST,
        getter=emails_getter,
    ),
    Window(
        Format(
        '''
            ℹ️\n
            • <b>Email:</b> {email.email}\n
            • <b>Sendments:</b {email.sendments}
        '''),
        Button(
        text='🗑️ Delete',
        id='email_deletion',
        on_click=email_deletion_handler,
        ),
        Back(Format('◀️')),
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
    getter=folders_getter,

)


# # Start(Format('📧 Emails'), state=FolderStatesGroup.FOLDER),
# Start(Format('💾 Add'), state=AddingEmailStatesGroup.EMAIL_INPUT),

# email_list_dialog = Dialog(
#     Window(
#         ScrollingGroup(
#             Select(
#                 id="email_select",
#                 items="emails",
#                 item_id_getter=lambda item: item.email,
#                 text=Format("📧 {item.email}"),
#                 on_click=selected_email_handler,
#             ),
#             id="email_group",
#             height=10,
#             width=2,
#             hide_on_single_page=True,
#             hide_pager=True
#         ),
#         Row(
#             PrevPage(
#                 scroll="email_group", text=Format("◀️"),
#             ),
#             CurrentPage(
#                 scroll="email_group", text=Format("{current_page1}"),
#             ),
#             NextPage(
#                 scroll="email_group", text=Format("▶️"),
#             ),
#         ),
#         state=EmailListSG.EMAIL_LIST,
#         getter=emails_getter,
#     ),
#     Window(
#         Format(
#         '''
#             ℹ️\n
#             • <b>Email:</b> {email.email}\n
#             • <b>Sendments:</b {email.sendments}
#         '''),
#         Button(
#         text='🗑️ Delete',
#         id='email_deletion',
#         on_click=email_deletion_handler,
#         ),
#         Back(Format('◀️')),
#         state=EmailListSG.EMAIL,
#         getter=get_one_email
#     ),
#     on_process_result=close_dialog,
# )