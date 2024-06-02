from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class UserModel(Base):
    __tablename__ = 'user'

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gmail: Mapped[Optional[str]] = mapped_column(String, nullable=True, unique=True)
    password: Mapped[Optional[str]] = mapped_column(String(16), nullable=True, unique=True)
    
    emails = relationship('EmailModel', back_populates='user')
    settings = relationship('SettingsModel', back_populates='user')
    folders = relationship('FolderModel', back_populates='user')
    mailing = relationship('MailingModel', back_populates='user')
