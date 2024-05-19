from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from dishka import FromDishka

from app.services import UserService
from app.bot.states import RegisterStatesGroup
from app.bot.keyboards import reply


router = Router()


@router.message(CommandStart())
async def start_handler(
    message: Message,
    user_service: FromDishka[UserService]
) -> None:
    user_id = message.from_user.id
    await user_service.save_user(user_id=user_id)
    await message.answer('hi', reply_markup=reply.menu_kb_markup)
    

@router.message(Command('register'))
async def register_handler(
    message: Message,
    state: FSMContext
) -> None:
    await message.answer('Type your email')
    await state.set_state(RegisterStatesGroup.EMAIL)

