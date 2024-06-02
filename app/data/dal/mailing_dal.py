from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, select, exists, delete, Result

from app.schemas import Mailing
from app.data.models import MailingModel


class MailingDAL:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, **kwargs) -> None:
        query = insert(MailingModel).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def update(self, job_id: int, **kwargs) -> None:
        query = update(MailingModel).where(MailingModel.job_id == job_id).values(**kwargs)

        await self.session.execute(query)
        await self.session.commit()

    async def exists(self, **kwargs) -> bool:
        query = select(
            exists().where(
                *(
                    getattr(MailingModel, key) == value
                    for key, value in kwargs.items()
                    if hasattr(MailingModel, key)
                )
            )
        )
        result = await self.session.execute(query)

        return result.scalar_one()

    async def is_column_filled(self, mailing_id: int, *column_names: str) -> bool:
        user_exists = await self.exists(user_id=mailing_id)

        if not user_exists:
            return False 

        query = select(
            *(
                getattr(MailingModel, column_name)
                for column_name in column_names
                if hasattr(MailingModel, column_name)
            )
        ).where(MailingModel.user_id == mailing_id)

        result = await self.session.execute(query)
        column_value = result.scalar_one_or_none()

        return column_value is not None

    async def _get(self, **kwargs) -> Result[tuple[MailingModel]] | None:
        exists = await self.exists(**kwargs)

        if not exists:
            return None

        query = select(MailingModel).filter_by(**kwargs)
        res = await self.session.execute(query)
        return res

    async def get_one(self, **kwargs) -> Mailing | None:
        res = await self._get(**kwargs)

        if res:
            db_mailing = res.scalar_one_or_none()
            return Mailing(
                job_id=db_mailing.job_id,
                folder_id=db_mailing.folder_id,
                user_id=db_mailing.user_id,
                scheduled_time=db_mailing.scheduled_time,
                is_active=db_mailing.is_active
            )

    async def get_all(self, **kwargs) -> list[Mailing] | None:
        res = await self._get(**kwargs)

        if res:
            db_mailings = res.scalars().all()
            return [
                Mailing(
                    job_id=db_mailing.job_id,
                    folder_id=db_mailing.folder_id,
                    user_id=db_mailing.user_id,
                    scheduled_time=db_mailing.scheduled_time,
                    is_active=db_mailing.is_active
                )
                for db_mailing in db_mailings
            ]

    async def delete(self, **kwargs) -> None:
        query = delete(MailingModel).filter_by(**kwargs)

        await self.session.execute(query)
        await self.session.commit()

