import datetime
from typing import Dict, Sequence

from aiogram_dialog import DialogManager

from dishka import FromDishka

from app.bot.bot_dialogs.getters.email_getter import inject_getter
from app.schemas import Folder, Settings, Mailing
from app.services import SettingsService, FolderService, ScheduledMailingService


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


async def scheduled_time_getter(
    dialog_manager: DialogManager,
    **kwargs
) -> Dict[Sequence[Settings], Sequence[Folder]]:  
    time = dialog_manager.dialog_data['time']
    date = dialog_manager.dialog_data['date']

    return {
        "date": date,
        "time": time,
    }


@inject_getter
async def mailings_info_getter(
    dialog_manager: DialogManager,
    scheduled_mailing_service: FromDishka[ScheduledMailingService],
    folder_service: FromDishka[FolderService],
    **kwargs
) -> Dict[str, Sequence[Mailing]]:
    job_id = dialog_manager.dialog_data['mailing_id']
    mailing = await scheduled_mailing_service.get_mailing(job_id=job_id, is_active=True)
    folder = await folder_service.get_folder(folder_id=mailing.folder_id)

    return {
        'mailing': mailing,
        "folder_name": folder.name
    }


@inject_getter
async def scheduled_mailings_getter(
    dialog_manager: DialogManager,
    scheduled_mailing_service: FromDishka[ScheduledMailingService],
    **kwargs,
) -> Dict[str, Sequence[Mailing]]:
    user = kwargs['event_from_user']
    mailings = await scheduled_mailing_service.get_mailings(user_id=user.id, is_active=True)
    mailings = list(filter(lambda m: m.scheduled_time > datetime.datetime.now(), mailings))

    return {
        'mailings': mailings,
        "is_empty": 0 if mailings else 1
    }
