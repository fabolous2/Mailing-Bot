
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, select, exists, delete, Result

from app.schemas import Email
from app.data.models import EmailModel


class EmailDAL:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, **kwargs) -> None:
        query = insert(EmailModel).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()


    async def exists(self, **kwargs) -> bool:
        query = select(
            exists().where(
                *(
                    getattr(EmailModel, key) == value
                    for key, value in kwargs.items()
                    if hasattr(EmailModel, key)
                )
            )
        )

        result = await self.session.execute(query)

        return result.scalar_one()


    async def _get(self, **kwargs) -> Result[tuple[EmailModel]] | None:
        exists = await self.exists(**kwargs)

        if not exists:
            return None

        query = select(EmailModel).filter_by(**kwargs)
        res = await self.session.execute(query)
        return res

    async def get_one(self, **kwargs) -> Email | None:
        res = await self._get(**kwargs)

        if res:
            db_email = res.scalar_one_or_none()
            return Email(
                id=db_email.id,
                user_id=db_email.user_id,
                email=db_email.email
            )

    async def get_all(self, **kwargs) -> list[Email] | None:
        res = await self._get(**kwargs)

        if res:
            db_emails = res.scalars().all()
            return [
                Email(
                    id=db_email.id,
                    user_id=db_email.user_id,
                    email=db_email.email
                )
                for db_email in db_emails
            ]

    async def delete(self, **kwargs) -> None:
        query = delete(EmailModel).where(
            {
                getattr(EmailModel, key) == value
                for key, value in kwargs.items()
                if hasattr(EmailModel, key)
            }
        )

        await self.session.execute(query)
        await self.session.commit()
