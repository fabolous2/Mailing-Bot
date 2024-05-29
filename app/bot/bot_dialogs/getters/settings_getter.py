from typing import Awaitable, Callable, Dict, Sequence

from aiogram_dialog import DialogManager

from dishka import FromDishka
from dishka.integrations.base import wrap_injection

from app.services import SettingsService
from app.schemas import Settings


def inject_getter(func: Callable) -> Awaitable:
    return wrap_injection(
        func=func,
        container_getter=lambda _, p: p["dishka_container"],
        is_async=True,
    )


@inject_getter
async def user_settings_getter(
    dialog_manager: DialogManager,
    settings_service: FromDishka[SettingsService],
    **kwargs
) -> Dict[str, Settings]:  
    user = kwargs['event_from_user']
    settings = await settings_service.get_settings(user_id=user.id)

    return {
        "settings": settings,
        "is_empty": 0 if settings else 1
    }

