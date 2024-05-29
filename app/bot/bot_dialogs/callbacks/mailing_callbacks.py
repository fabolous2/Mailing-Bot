from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import (
    Select,
    Button
)

from dishka import FromDishka

from app.bot.bot_dialogs.callbacks.wrappers import inject_on_click
from app.bot.states import MailingStatesGroup
from app.services import MailingService


async def selected_folder(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: int,
) -> None:
    dialog_manager.dialog_data["folder_id"] = item_id
    await dialog_manager.switch_to(MailingStatesGroup.MAILING)


async def cancel_mailing_handler(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    await callback_query.answer('✅ Вы успешно отменили отправку!')
    await callback_query.message.delete()
    await dialog_manager.done()


@inject_on_click
async def mailing_handler(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    mailing_service: FromDishka[MailingService],
) -> None:
    audio_list = dialog_manager.dialog_data['attachment_audio']
    folder_id = dialog_manager.dialog_data['folder_id']
    bot = callback_query.message.bot
    for audio in audio_list:
        audio_file_info = await bot.get_file(audio.file_id)
        audio_data = await bot.download_file(audio_file_info.file_path)
        await mailing_service.attach_audio(audio_data=audio_data, filename=audio.file_name)
        
    await mailing_service.send_email(user_id=callback_query.from_user.id, folder_id=folder_id)