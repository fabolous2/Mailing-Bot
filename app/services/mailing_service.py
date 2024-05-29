from typing import Dict, Tuple, Sequence, Optional
from io import BytesIO

from aiosmtplib import SMTP, SMTPResponse

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase

from app.services import SettingsService, EmailService, UserService
from app.schemas import User, Settings


class MailingService:
    _client: SMTP = SMTP(
        hostname='smtp.gmail.com',
        port=587,
        start_tls=True,
        validate_certs=False,
    )

    def __init__(
        self,
        settings_service: SettingsService,
        email_service: EmailService,
        user_service: UserService,
    ) -> None:
        self.settings_service = settings_service
        self.email_service = email_service
        self.user_service = user_service
        self._email_message = MIMEMultipart()

        self._user: User = None
        self._settings: Settings = None

    async def _attach_message(self, folder_id: int) -> None:
        self._settings = await self.settings_service.get_settings(folder_id=folder_id)
    
        self._email_message['Subject'] = self._settings.subject
        self._email_message['From'] = self._user.email
        self._email_message.attach(MIMEText(self._settings.text, "plain", "utf-8"))
    
    async def _recipients(self, folder_id: int) -> Optional[Sequence[str]]:
        recipients = await self.email_service.get_emails(folder_id=folder_id)
        recipients = [email_item.email for email_item in recipients]
        return recipients

    async def _send(self, recipients: Optional[Sequence[str]]) -> Tuple[Dict[str, SMTPResponse], str]:
        try:
            await self._client.sendmail(
                self._user.email,
                recipients,
                self._email_message.as_string()
            )
        except Exception as _ex:
            print(_ex)
        finally:
            await self._client.quit()
        
    async def attach_audio(self, audio_data: BytesIO, filename: str) -> None:
        file = MIMEBase('audio', 'mp3')
        file.set_payload(audio_data.read())
        encoders.encode_base64(file)
        file.add_header('content-disposition','attachment', filename=filename)
        self._email_message.attach(file)
    
    async def send_email(
        self,
        user_id: int,
        folder_id: int,
    ) -> None:
        self._user = await self.user_service.get_user(user_id=user_id)
        recipients = await self._recipients(folder_id=folder_id)

        await self._client.connect(username=self._user.email, password=self._user.password)
        await self._attach_message(folder_id=folder_id)
        await self._send(recipients=recipients)

