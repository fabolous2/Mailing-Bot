from typing import Dict, Sequence

from aiogram_dialog import DialogManager

from dishka import FromDishka

from app.bot.bot_dialogs.getters.email_getter import inject_getter
from app.schemas import Folder, Settings
from app.services import SettingsService, FolderService


@inject_getter
async def mail_getter(
    dialog_manager: DialogManager,
    settings_service: FromDishka[SettingsService],
    folder_service: FromDishka[FolderService],
    **kwargs
) -> Dict[Sequence[Settings], Sequence[Folder]]:  
    folder_id = dialog_manager.dialog_data['folder_id']
    settings = await settings_service.get_settings(folder_id=folder_id)
    folder = await folder_service.get_folder(folder_id=folder_id)

    return {
        "settings": settings,
        "folder": folder
    }