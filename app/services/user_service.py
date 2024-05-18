from app.schemas import User
from app.data.dal import UserDAL, EmailSettingsDAL


class UserService:
    def __init__(self, user_dal: UserDAL, settings_dal: EmailSettingsDAL) -> None:
        self.user_dal = user_dal
        self.settings_dal = settings_dal
    
    async def save_user(self, user: User) -> None:
        exists = await self.user_dal.exists(user_id=user.user_id)

        if not exists:
            await self.user_dal.add(user)

    async def update_user(self, user_id: int, **kwargs) -> None:
        await self.user_dal.update(user_id, **kwargs)

    async def user_is_registered(self, user_id: int) -> bool:
        return await self.user_dal.is_column_filled(user_id, "personal_email", "password")