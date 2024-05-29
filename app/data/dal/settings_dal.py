from sqlalchemy import insert, select, exists, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import Settings
from app.data.models import SettingsModel


class SettingsDAL:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
     
    async def update(self, folder_id: int, **kwargs) -> None:
        query = update(SettingsModel).where(SettingsModel.folder_id == folder_id).values(**kwargs)

        await self.session.execute(query)
        await self.session.commit()
      
    async def exists(self, **kwargs) -> bool:
        query = select(exists().where(
            *(getattr(SettingsModel, key) == value for key, value in kwargs.items() if hasattr(SettingsModel, key))
        ))

        result = await self.session.execute(query)
        return result.scalar_one()

    async def add(self, **kwargs) -> None:
        query = insert(SettingsModel).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def get_one(self, **kwargs) -> Settings:
        exists = await self.exists(**kwargs)

        if not exists:
            return None
        
        query = select(SettingsModel).filter_by(**kwargs)
        results = await self.session.execute(query)
        db_settings = results.scalar_one()

        return Settings(
            id=db_settings.id,
            user_id=db_settings.user_id,
            folder_id=db_settings.folder_id,
            subject=db_settings.subject,
            text=db_settings.text,
        )

    async def get_all(self, **kwargs) -> list[Settings]:
        exists = await self.exists(**kwargs)
        
        if not exists:
            return None
        
        query = select(SettingsModel).filter_by(**kwargs)
        results = await self.session.execute(query)
        db_settings = results.scalars().all()

        return [
            Settings(
                id=db_setting.id,
                user_id=db_setting.user_id,
                folder_id=db_setting.folder_id,
                subject=db_setting.subject,
                text=db_setting.text,
            ) for db_setting in db_settings
        ]
