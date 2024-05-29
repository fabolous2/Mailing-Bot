from app.schemas import Settings
from app.data.dal import SettingsDAL


class SettingsService:
    def __init__(self, settings_dal: SettingsDAL) -> None:
        self.settings_dal = settings_dal

    async def update_settings(self, folder_id: int, **kwargs) -> None:
        await self.settings_dal.update(folder_id, **kwargs)

    async def get_settings(self, **kwargs) -> Settings:
        settings = await self.settings_dal.get_one(**kwargs)
        return settings
    
    async def add_settings(self, **kwargs) -> None:
        exists = await self.settings_dal.exists(**kwargs)
        if not exists:
            await self.settings_dal.add(**kwargs)
