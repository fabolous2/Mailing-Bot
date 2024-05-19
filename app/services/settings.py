from app.schemas import Settings
from app.data.dal import SettingsDAL


class SettingsService:
    def __init__(self, settings_dal: SettingsDAL) -> None:
        self.settings_dal = settings_dal

    async def update_settings(self, user_id: int, **kwargs) -> None:
        await self.settings_dal.update(user_id, **kwargs)

    async def get_settings(self, user_id: int) -> Settings:
        settings = await self.settings_dal.get_one(user_id=user_id)
        return settings
    
    async def add_settings(self, **kwargs) -> None:
        exists = await self.settings_dal.exists(**kwargs)
        if not exists:
            await self.settings_dal.add(**kwargs)
