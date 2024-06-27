from typing import Sequence

from app.data.dal import MailingDAL
from app.schemas import Mailing


class ScheduledMailingService:
    def __init__(self, mailing_dal: MailingDAL) -> None:
        self.mailing_dal = mailing_dal

    async def add(self, **kwargs) -> None:
        await self.mailing_dal.add(**kwargs)

    async def get_mailings(self, **kwargs) -> Sequence[Mailing] | None:
        mailing = await self.mailing_dal.get_all(**kwargs)
        return mailing
    
    async def get_mailing(self, **kwargs) -> Mailing | None:
        mailing = await self.mailing_dal.get_one(**kwargs)
        return mailing

    async def update(self, job_id: int, **kwargs) -> None:
        await self.mailing_dal.update(job_id=job_id, **kwargs)
    
