from typing import Sequence, Dict 

from app.data.dal import EmailDAL
from app.schemas import Email


class EmailService:
    def __init__(self, email_dal: EmailDAL) -> None:
        self.email_dal = email_dal

    async def add_emails(self, emails: Sequence[str]) -> None:
        await self.email_dal.add(emails)

    async def get_emails(self, **kwargs) -> Sequence[Email] | None:
        emails = await self.email_dal.get_all(**kwargs)
        return emails
    
    async def get_email(self, **kwargs) -> Email | None:
        email = await self.email_dal.get_one(**kwargs)
        return email
    
    async def delete_emails(self, emails: Sequence[str]) -> None:
        return await self.email_dal.delete(emails=emails)
    
    async def update_index(self, emails: Sequence[Dict]) -> None:
        for email in emails:
            email.email_index += 1
        
        await self.email_dal.update(emails=emails)
