from typing import Sequence, Dict 
from dataclasses import asdict, astuple

from app.data.dal import EmailDAL
from app.schemas import Email


class EmailService:
    def __init__(self, email_dal: EmailDAL) -> None:
        self.email_dal = email_dal

    async def formate_list(
        self,
        email_list: Sequence[str],
        user_id: int,
        folder_id: int
    ) -> Sequence[Dict[str, str | int]]:
        email_list = [
            {
                'user_id': user_id,
                'email': email,
                'folder_id': folder_id
            }
            for email in email_list
        ]
        return email_list

    async def add_emails(self, email_list: Sequence[Dict[str, str | int]]) -> None:
        await self.email_dal.add(email_list=email_list)

    async def get_emails(self, **kwargs) -> Sequence[Email] | None:
        emails = await self.email_dal.get_all(**kwargs)
        return emails
    
    async def get_email(self, **kwargs) -> Email | None:
        email = await self.email_dal.get_one(**kwargs)
        return email
    
    async def delete_email(self, **kwargs) -> None:
        await self.email_dal.delete(**kwargs)
    
    async def update_index(self, emails: Sequence[Dict]) -> None:
        for email in emails:
            email.email_index += 1
        
        await self.email_dal.update(emails=emails)
