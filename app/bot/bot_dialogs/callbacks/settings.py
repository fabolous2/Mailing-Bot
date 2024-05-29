from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import (
    Select,
    Button
)
from aiogram_dialog.widgets.input import ManagedTextInput

from dishka import FromDishka

from app.bot.states import SettingsStatesGroup
from app.services import SettingsService
from .wrappers import inject_on_process_result, inject_on_click


async def selected_folder(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: int,
) -> None:
    dialog_manager.dialog_data["folder_id"] = item_id
    await dialog_manager.switch_to(SettingsStatesGroup.MAIN_MENU)


@inject_on_process_result
async def on_input_subject(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    value: str,
    settings_service: FromDishka[SettingsService],
) -> None:
    subject = value
    folder_id = dialog_manager.dialog_data['folder_id']

    try:
        await settings_service.update_settings(
            folder_id=folder_id,
            subject=subject
        )
    except Exception as _ex:
        print(_ex)
    finally:
        await dialog_manager.switch_to(SettingsStatesGroup.MAIN_MENU)


@inject_on_process_result
async def on_input_message(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    value: str,
    settings_service: FromDishka[SettingsService],
) -> None:
    text = value
    folder_id = dialog_manager.dialog_data['folder_id']

    try:
        await settings_service.update_settings(
            folder_id=folder_id,
            text=text
        )
    except Exception as _ex:
        print(_ex)
    finally:
        await dialog_manager.switch_to(SettingsStatesGroup.MAIN_MENU)


@inject_on_click
async def switch_to_message_input(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(SettingsStatesGroup.MESSAGE_INPUT)


@inject_on_click
async def switch_to_subject_input(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(SettingsStatesGroup.SUBJECT_INPUT)