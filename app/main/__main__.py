import logging
import asyncio

from dishka.integrations.aiogram import setup_dishka
from dishka import make_async_container

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder

from aiogram_dialog import setup_dialogs

from aiogram_album.ttl_cache_middleware import TTLCacheAlbumMiddleware
from aiogram.client.session.aiohttp import AiohttpSession

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler_di import ContextSchedulerDecorator
from apscheduler.jobstores.redis import RedisJobStore

from redis.asyncio.client import Redis

from app.main.config import settings
from app.main.ioc import DatabaseProvider, DALProvider, ServiceProvider
from app.bot import routers
from app.bot.bot_dialogs import dialogs
from app.bot.middlewares.scheduler import SchedulerMiddleware


logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    storage = RedisStorage(Redis(db=2), key_builder=DefaultKeyBuilder(with_destiny=True))
    jobstores = {
        'default': RedisJobStore(
            jobs_key='dispatched_trips_jobs',
            run_times_key='dispatched_trips_running',
            host='localhost',
            db=2,
            port=6379
        )
    }
    scheduler = ContextSchedulerDecorator(AsyncIOScheduler(timezone="Europe/Moscow", jobstores=jobstores))

    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dispatcher = Dispatcher(storage=storage, scheduler=scheduler)
    scheduler.ctx.add_instance(instance=bot, declared_class=Bot)

    dispatcher.include_routers(*routers)
    dispatcher.include_routers(*dialogs)

    TTLCacheAlbumMiddleware(router=dispatcher)
    dispatcher.message.middleware.register(SchedulerMiddleware(scheduler=scheduler))

    container = make_async_container(DatabaseProvider(), DALProvider(), ServiceProvider())
    setup_dishka(container=container, router=dispatcher, auto_inject=True)
    setup_dialogs(dispatcher)

    try:
        scheduler.start()
        await bot.delete_webhook(drop_pending_updates=True)
        await dispatcher.start_polling(bot, skip_updates=True)
    finally:
        scheduler.shutdown()
        await dispatcher.storage.close()
        await container.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")