import datetime

from sqlalchemy import Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class MailingModel(Base):
    __tablename__ = 'mailing'

    job_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    folder_id: Mapped[int] = mapped_column(Integer, ForeignKey('folder.folder_id'))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.user_id'))
    scheduled_time: Mapped[datetime.datetime] = mapped_column(DateTime)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    user = relationship('UserModel', back_populates='mailing')
    folder = relationship('FolderModel', back_populates='mailing')