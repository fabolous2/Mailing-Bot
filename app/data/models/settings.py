from typing import Optional
from datetime import datetime

from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class SettingsModel(Base):
    __tablename__ = "email_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'))
    folder_id: Mapped[int] = mapped_column(Integer, ForeignKey('folder.folder_id', ondelete='CASCADE'))
    subject: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    text: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    folder = relationship('FolderModel', back_populates='settings')
    user = relationship('UserModel', back_populates='settings')