from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == '📨 Mailing')
async def mailing_handler(
    message: Message,
) -> None:
    pass


@router.message(F.text == '📪 Emails')
async def email_handler(
    message: Message,
) -> None:
    pass


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