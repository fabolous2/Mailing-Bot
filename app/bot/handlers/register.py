import re

from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from dishka import FromDishka

from app.services import UserService
from app.bot.states import RegisterStatesGroup


router = Router()


@router.message(RegisterStatesGroup.EMAIL)
async def register_email_handler(message: Message, state: FSMContext) -> None:
    email = message.text
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if not re.match(email_pattern, email):
        await message.answer("Почта введена неверно. Попробуйте еще раз!")
    else:
        await state.update_data(email=email)
        await state.set_state(RegisterStatesGroup.PASSWORD)
        await message.answer('You successfully set an email! Type your application password.')
    

@router.message(RegisterStatesGroup.PASSWORD)
async def register_password_handler(
    message: Message,
    state: FSMContext,
    user_service: FromDishka[UserService],
) -> None:
    password = message.text
    user_id = message.from_user.id

    if (
        len(password) < 19
        or len(password) > 20
        or re.search(r"\d", password)
        or not password.count(" ") == 3
    ):
        await message.answer('Password is invalid... Try again.')
    else:
        state_data = state.get_data()
        try:
            await user_service.update_user(
                user_id=user_id,
                email=state_data['email'],
                password=password,
            )
            await message.answer('You succesfully connected your email account!')
        except Exception as _ex:
            print(_ex)
            await message.answer('Oopps... Something wrong(')
        finally:
            await state.clear()
