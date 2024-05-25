from aiogram import Router, F
from aiogram.types import Message

from aiogram_dialog import DialogManager, ShowMode, StartMode

from app.bot.states import FolderStatesGroup, AddingEmailStatesGroup

router = Router()


@router.message(F.text == '📨 Mailing')
async def mailing_handler(
    message: Message,
) -> None:
    pass


@router.message(F.text == '📪 Emails')
async def email_handler(
    message: Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(
        state=FolderStatesGroup.FOLDER_SELECTION, 
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT
    )


@router.message(F.text == '🎶 Beats')
async def audio_handler(
    message: Message,
) -> None:
    pass


@router.message(F.text == '⚙️ Settings')
async def settings_handler(
    message: Message,
) -> None:
    pass


@router.message(F.text)
async def echo(
    message: Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(AddingEmailStatesGroup.CHECK_OUT)
    dialog_manager.dialog_data['email_list'] = message.replace(',', ' ').split()