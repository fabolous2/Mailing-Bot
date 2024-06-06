import datetime
import random
import time

from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import (
    Select,
    Button
)
from aiogram_dialog.widgets.input import ManagedTextInput

from dishka import FromDishka

from apscheduler_di.decorator import AsyncIOScheduler

from app.bot.bot_dialogs.callbacks.wrappers import inject_on_click, inject_on_process_result
from app.bot.states import MailingStatesGroup, ScheduledMailingSG
from app.services import MailingService, ScheduledMailingService


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
        audio_file_info = await bot.get_file(audio['file_id'])
        audio_data = await bot.download_file(audio_file_info.file_path)
        await mailing_service.attach_audio(audio_data=audio_data, filename=audio['file_name'])
        
    await mailing_service.send_email(user_id=callback_query.from_user.id, folder_id=folder_id)


async def schedule_mailing_handler(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(MailingStatesGroup.SCHEDULER)


async def on_date_selected(
    callback: CallbackQuery,
    widget,
    manager: DialogManager,
    selected_date: datetime.date
) -> None:
    print('date handler works')
    manager.dialog_data['date'] = str(selected_date)
    print('date works 2')
    await manager.switch_to(MailingStatesGroup.TIME)


async def on_input_time(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    value: str,
) -> None:
    print('time handler works')
    time = datetime.time(hour=int(value[:2]), minute=int(value[3:]))
    dialog_manager.dialog_data['time'] = str(time)
    print('time works 2')
    await dialog_manager.switch_to(MailingStatesGroup.SCHEDULE_MAILING)


async def cancel_scheduling(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    await callback_query.answer('Scheduling was successfilly canceled!', show_alert=True)
    await dialog_manager.switch_to(MailingStatesGroup.MAILING)


@inject_on_click
async def confirm_scheduling(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    mailing_service: FromDishka[MailingService],
    scheduled_mailing_service: FromDishka[ScheduledMailingService],
) -> None:
    user_id = callback_query.from_user.id
    audio_list = dialog_manager.dialog_data['attachment_audio']
    folder_id = dialog_manager.dialog_data['folder_id']
    date = dialog_manager.dialog_data['date']
    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    time_on = dialog_manager.dialog_data['time']
    print(time_on)
    time_on = datetime.time(hour=int(time_on[:2]), minute=int(time_on[3:5]))

    combined_datetime = datetime.datetime.combine(date, time_on)
    job_id = str(int(time.time()) + random.randint(0, 99999))

    try:
        await mailing_service.schedule(
            user_id=user_id,
            folder_id=folder_id,
            audio_list=audio_list,
            bot=callback_query.message.bot,
            run_date=combined_datetime,
            job_id=job_id
        )
        await scheduled_mailing_service.add(
            job_id=int(job_id),
            folder_id=folder_id,
            user_id=user_id,
            scheduled_time=combined_datetime
        )
        await callback_query.answer('Вы успешно установили расписание вашей отправки!', show_alert=True)
        await callback_query.message.delete()
    except Exception as _ex:
        print(_ex)
    finally:
        await dialog_manager.done()


async def selected_mailing(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: int,
) -> None:
    dialog_manager.dialog_data["mailing_id"] = item_id
    await dialog_manager.switch_to(ScheduledMailingSG.MAILING_INFO)


@inject_on_click
async def cancel_sheduled_mailing_task(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    scheduled_mailing_service: FromDishka[ScheduledMailingService],
    mailing_service: FromDishka[MailingService],
) -> None:
    job_id = dialog_manager.dialog_data["mailing_id"]
    await mailing_service.cancel_mailing(
        job_id=str(job_id),
    )
    await callback_query.answer("Вы успешно отменили рассылку!", show_alert=True)
    await dialog_manager.back()

    