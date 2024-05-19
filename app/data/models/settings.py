from typing import Optional
from datetime import datetime

from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class SettingsModel(Base):
    __tablename__ = "email_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'))
    audio_amount: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    schedule: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    subject: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    text: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    turned_on: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)

    user = relationship('UserModel', back_populates='settings')