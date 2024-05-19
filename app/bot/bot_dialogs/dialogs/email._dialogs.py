from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import (
    ScrollingGroup,
    Select,
    Row,
    PrevPage,
    NextPage,
    CurrentPage,
    Back,
    Start
)

from app.bot.states import AddingEmailStatesGroup, EmailListSG


async def close_dialog(_, __, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.done()


email_main_dialog = Dialog(
    Window(
        ScrollingGroup(
            Select(
                id="folder_select",
                items="folders",
                item_id_getter=lambda item: item.name,
                text=Format("№{item.name}"),
                on_click=selected_OrderSlot,
            ),
            id="folder_group",
            height=10,
            width=1,
            hide_on_single_page=True,
            hide_pager=True
        ),
        Start(
            Format('New folder')
        )
    ),

)


# Start(Format('📧 Emails'), state=EmailListSG.FOLDER),
# Start(Format('💾 Add'), state=AddingEmailStatesGroup.EMAIL_INPUT),

email_list_dialog = Dialog(
        Window(
        ScrollingGroup(
            Select(
                id="audio_select",
                items="audios",
                item_id_getter=lambda item: item.email,
                text=Format("№{item.email}"),
                on_click=selected_OrderSlot,
            ),
            id="audio_group",
            height=10,
            width=2,
            hide_on_single_page=True,
            hide_pager=True
        ),
        Row(
            PrevPage(
                scroll="audio_group", text=Format("◀️"),
            ),
            CurrentPage(
                scroll="audio_group", text=Format("{current_page1}"),
            ),
            NextPage(
                scroll="audio_group", text=Format("▶️"),
            ),
        ),
        state=OrderSelection.order_selection,
        getter=get_orders,
    ),
    Window(
        Format(''),
        Back(Format('◀️')),
    state=OrderSelection.order_info,
    getter=get_one_order
    ),
    on_process_result=close_dialog,
)