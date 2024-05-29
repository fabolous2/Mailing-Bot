from app.data.dal import UserDAL
from app.schemas import User

class UserService:
    def __init__(self, user_dal: UserDAL) -> None:
        self.user_dal = user_dal
    
    async def save_user(self, **kwargs) -> None:
        exists = await self.user_dal.exists(**kwargs)

        if not exists:
            await self.user_dal.add(**kwargs)

    async def update_user(self, user_id: int, **kwargs) -> None:
        await self.user_dal.update(user_id, **kwargs)

    async def user_is_registered(self, user_id: int) -> bool:
        return await self.user_dal.is_column_filled(user_id, "personal_email", "password")
    
    async def get_user(self, user_id: int) -> User:
        return await self.user_dal.get_one(user_id=user_id)