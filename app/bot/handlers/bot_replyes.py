from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from aiogram_dialog import DialogManager, StartMode

from aiogram_album import AlbumMessage

from app.bot.states import FolderStatesGroup, SettingsStatesGroup, MailingStatesGroup, ScheduledMailingSG

router = Router()


@router.message(F.text == '📨 Mailing')
async def mailing_handler(
    message: Message,
    state: FSMContext
) -> None:
    await message.answer('🎵 Отправьте аудио')
    await state.set_state(MailingStatesGroup.AUDIOS)


@router.message(MailingStatesGroup.AUDIOS, F.audio)
async def single_audio_handler(
    message: Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=MailingStatesGroup.FOLDER_SELECTION, mode=StartMode.RESET_STACK)
    dialog_manager.dialog_data['attachment_audio'] = [{
        'file_id': message.audio.file_id,
        'file_name': message.audio.file_name
    }]


@router.message(MailingStatesGroup.AUDIOS, F.media_group_id)
async def audios_handler(
    messages: AlbumMessage,
    dialog_manager: DialogManager,
) -> None:
    audios = [{
        'file_id': message.audio.file_id,
        'file_name': message.audio.file_name
    } for message in messages]
    await dialog_manager.start(state=MailingStatesGroup.FOLDER_SELECTION, mode=StartMode.RESET_STACK)
    dialog_manager.dialog_data['attachment_audio'] = audios
    

@router.message(F.text == '📪 Emails')
async def email_handler(
    message: Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=FolderStatesGroup.FOLDER_SELECTION, mode=StartMode.RESET_STACK)


@router.message(F.text == '⚙️ Settings')
async def settings_handler(
    message: Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(SettingsStatesGroup.FOLDER_SELECTION, mode=StartMode.RESET_STACK)


@router.message(F.text == '⌛ Scheduled')
async def scheduled_handler(
    message: Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(ScheduledMailingSG.MAILING_SELECTION, mode=StartMode.RESET_STACK)
    