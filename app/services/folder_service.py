from typing import Sequence

from app.data.dal import FolderDAL
from app.schemas import Folder


class FolderService:
    def __init__(self, folder_dal: FolderDAL) -> None:
        self.folder_dal = folder_dal

    async def add_folder(self, **kwargs) -> None:
        await self.folder_dal.add(**kwargs)

    async def get_folders(self, **kwargs) -> Sequence[Folder] | None:
        emails = await self.folder_dal.get_all(**kwargs)
        return emails
    
    async def get_folder(self, **kwargs) -> Folder | None:
        email = await self.folder_dal.get_one(**kwargs)
        return email
    
    async def delete_folder(self, **kwargs) -> None:
        return await self.folder_dal.delete(**kwargs)
    
