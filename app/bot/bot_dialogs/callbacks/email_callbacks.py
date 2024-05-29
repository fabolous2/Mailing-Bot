import random

from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select, Button
from aiogram_dialog.widgets.input import ManagedTextInput

from dishka import FromDishka

from app.bot.states import FolderStatesGroup, AddingEmailStatesGroup
from app.services import FolderService, EmailService
from app.services.settings import SettingsService
from .wrappers import inject_on_click, inject_on_process_result


async def selected_folder(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: int,
) -> None:
    dialog_manager.dialog_data["folder_id"] = item_id
    await dialog_manager.switch_to(FolderStatesGroup.FOLDER)


async def deletion_check_out(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager, 
) -> None:
    await dialog_manager.switch_to(FolderStatesGroup.FOLDER_DELETION)


@inject_on_click
async def delete_folder(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    folder_service: FromDishka[FolderService],
) -> None:
    folder_id = dialog_manager.dialog_data['folder_id']
    try:
        await folder_service.delete_folder(folder_id=folder_id)
        await callback_query.answer('❗Folder was successfully deleted.', show_alert=True)
    except Exception as _ex:
        print(_ex)
        await callback_query.answer('⚠️ Something wrong...')
    finally:
        await dialog_manager.switch_to(FolderStatesGroup.FOLDER_SELECTION)


async def cancel_folder_deletion_handler(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.back()


async def add_folder_handler(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(FolderStatesGroup.FOLDER_CREATION)


@inject_on_process_result
async def on_input_folder_name(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    value: str,
    folder_service: FromDishka[FolderService],
    settings_service: FromDishka[SettingsService],
) -> None:
    user_id = message.from_user.id
    folder_id = int(f'{user_id}{random.randint(0, 9999)}')

    try:
        await folder_service.add_folder(
            name=value,
            user_id=user_id,
            folder_id=folder_id,
        )
        await settings_service.add_settings(
            user_id=user_id,
            folder_id=folder_id
        )
    except Exception as _ex:
        print(_ex)
        await message.answer('⚠️ Something wrong...')
    finally:
        await dialog_manager.switch_to(FolderStatesGroup.FOLDER_SELECTION)


async def selected_email_handler(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    item_id: str,   
) -> None:
    dialog_manager.dialog_data['email'] = item_id
    await dialog_manager.switch_to(state=FolderStatesGroup.EMAIL)


@inject_on_click
async def email_deletion_handler(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    email_service: FromDishka[EmailService],
) -> None:
    email = dialog_manager.dialog_data['email']
    user_id = callback_query.from_user.id
    print(email)
    try:
        await email_service.delete_email(user_id=user_id, email=email)
        await callback_query.answer('🗑️ Email was successfully deleted!')
    except Exception as _ex:
        print(_ex)
        await callback_query.answer('⚠️ Something wrong...', show_alert=True)
    finally:
        await dialog_manager.switch_to(FolderStatesGroup.EMAIL_LIST)


async def switch_to_email_list(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(FolderStatesGroup.EMAIL_LIST)


async def back_to_folder(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(FolderStatesGroup.FOLDER)


async def email_addition_handler(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager, 
) -> None:
    await dialog_manager.switch_to(FolderStatesGroup.EMAIL_ADDITION)
    

@inject_on_process_result
async def on_input_emails(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    value: str,
    email_service: FromDishka[EmailService],
) -> None:
    user_id = message.from_user.id
    email_list = value.replace(',', ' ').split()
    folder_id = dialog_manager.dialog_data['folder_id']

    try:
        fomatted_list = await email_service.formate(
            user_id=user_id,
            folder_id=folder_id,
            email_list=email_list
        )
        await email_service.add_emails(email_list=fomatted_list)
        await message.answer('🎉 successfully added')
    except Exception as _ex:
        print(_ex)
        await message.answer('⚠️ Something wrong...')
    finally:
        await dialog_manager.switch_to(state=FolderStatesGroup.EMAIL_LIST)


@inject_on_process_result
async def on_select_folder_for_adding(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    item_id: int,
    email_service: FromDishka[EmailService],
) -> None:
    user_id = callback_query.from_user.id
    email_list = dialog_manager.dialog_data['email_list']
    folder_id = item_id

    try:
        email_list = email_list.replace(',', ' ').split()
        print(email_list)
        fomatted_list = await email_service.formate(
            user_id=user_id,
            folder_id=folder_id,
            email_list=email_list
        )
        await email_service.add_emails(email_list=fomatted_list)
    except Exception as _ex:
        print(_ex)
        await callback_query.answer('⚠️ Something wrong...', show_alert=True)
    finally:
        await dialog_manager.switch_to(AddingEmailStatesGroup.SUCCESS)


async def on_confirm_adding(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(AddingEmailStatesGroup.FOLDER_SELECTION)


async def on_cancel_adding(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager, 
) -> None:
    await callback_query.message.delete()
    await callback_query.answer('Canceled')
    await dialog_manager.close_manager()