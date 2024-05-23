from typing import Awaitable, Callable, Dict, Sequence

from aiogram_dialog import DialogManager

from dishka import FromDishka
from dishka.integrations.base import wrap_injection

from app.services import FolderService, EmailService
from app.schemas import Folder, Email


def inject_getter(func: Callable) -> Awaitable:
    return wrap_injection(
        func=func,
        container_getter=lambda _, p: p["dishka_container"],
        is_async=True,
    )


@inject_getter
async def folders_getter(
    dialog_manager: DialogManager,
    folder_service: FromDishka[FolderService],
    **kwargs
) -> Dict[str, Sequence[Folder]]:  
    user = kwargs['event_from_user']
    folders = await folder_service.get_folders(user_id=user.id)

    return {
        "folders": folders,
        "is_empty": 0 if folders else 1
    }


@inject_getter
async def emails_getter(
    dialog_manager: DialogManager,
    email_service: FromDishka[EmailService],
    **kwargs
) -> Dict[str, Sequence[Email]]:
    folder_id = dialog_manager.dialog_data['folder_id']
    email_list = await email_service.get_emails(folder_id=folder_id)
    
    return {
        'emails': email_list,
        'is_empty': 0 if email_list else 1
    }


@inject_getter
async def get_one_email(
    dialog_manager: DialogManager,
    email_service: FromDishka[EmailService],
    **kwargs
) -> Dict[str, Email]:
    email = dialog_manager.dialog_data['email']
    user = kwargs['event_from_user']
    email = await email_service.get_email(user_id=user.id, email=email)

    return {
        'email': email
    }