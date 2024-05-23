from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, select, exists, delete, Result

from app.schemas import Folder
from app.data.models import FolderModel


class FolderDAL:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, **kwargs) -> None:
        query = insert(FolderModel).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()


    async def exists(self, **kwargs) -> bool:
        query = select(
            exists().where(
                *(
                    getattr(FolderModel, key) == value
                    for key, value in kwargs.items()
                    if hasattr(FolderModel, key)
                )
            )
        )

        result = await self.session.execute(query)

        return result.scalar_one()


    async def _get(self, **kwargs) -> Result[tuple[FolderModel]] | None:
        exists = await self.exists(**kwargs)

        if not exists:
            return None

        query = select(FolderModel).filter_by(**kwargs)
        res = await self.session.execute(query)
        return res

    async def get_one(self, **kwargs) -> Folder | None:
        res = await self._get(**kwargs)

        if res:
            db_folder = res.scalar_one_or_none()
            return Folder(
                folder_id=db_folder.folder_id,
                user_id=db_folder.user_id,
                name=db_folder.name,
            )

    async def get_all(self, **kwargs) -> Sequence[Folder] | None:
        res = await self._get(**kwargs)

        if res:
            db_folders = res.scalars().all()
            return [
                Folder(
                    folder_id=db_folder.folder_id,
                    user_id=db_folder.user_id,
                    name=db_folder.name,
                )
                for db_folder in db_folders
            ]

    async def delete(self, **kwargs) -> None:
        query = delete(FolderModel).filter_by(**kwargs)

        await self.session.execute(query)
        await self.session.commit()

