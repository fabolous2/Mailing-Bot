from typing import AsyncGenerator

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from app.main.config import settings
from app.data.dal import UserDAL, EmailDAL, AudioDAL, SettingsDAL, FolderDAL
from app.services import UserService, EmailService, AudioService, SettingsService, FolderService, MailingService


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP, provides=AsyncEngine)
    def get_engine(self) -> AsyncEngine:
        return create_async_engine(url=settings.DATABASE_URL)

    @provide(scope=Scope.APP, provides=async_sessionmaker[AsyncSession])
    def get_async_sessionmaker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=engine)

    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def get_async_session(self, sessionmaker: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
        async with sessionmaker() as session:
            yield session


class DALProvider(Provider):
    user_dal = provide(UserDAL, scope=Scope.REQUEST, provides=UserDAL)
    email_dal = provide(EmailDAL, scope=Scope.REQUEST, provides=EmailDAL)
    audio_dal = provide(AudioDAL, scope=Scope.REQUEST, provides=AudioDAL)
    settings_dal = provide(SettingsDAL, scope=Scope.REQUEST, provides=SettingsDAL)
    folder_dal = provide(FolderDAL, scope=Scope.REQUEST, provides=FolderDAL)


class ServiceProvider(Provider):
    user_service = provide(UserService, scope=Scope.REQUEST, provides=UserService)
    email_service = provide(EmailService, scope=Scope.REQUEST, provides=EmailService)
    audio_service = provide(AudioService, scope=Scope.REQUEST, provides=AudioService)
    settings_service = provide(SettingsService, scope=Scope.REQUEST, provides=SettingsService)
    folder_service = provide(FolderService, scope=Scope.REQUEST, provides=FolderService)
    mailing_service = provide(MailingService, scope=Scope.REQUEST, provides=MailingService)
