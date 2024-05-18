import logging
import asyncio

from dishka.integrations.aiogram import setup_dishka
from dishka import make_async_container

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from app.main.config import settings
from app.main.ioc import DatabaseProvider, DALProvider, ServiceProvider


logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    storage = MemoryStorage()
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dispatcher = Dispatcher(storage=storage)

    dispatcher.include_routers(
        ...
        )

    container = make_async_container(DatabaseProvider(), DALProvider(), ServiceProvider())
    setup_dishka(container=container, router=dispatcher, auto_inject=True)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dispatcher.start_polling(bot, skip_updates=True)
    finally:
        await container.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")