from typing import Optional

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class EmailModel(Base):
    __tablename__ = 'user_email'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.user_id'))
    email: Mapped[str] = mapped_column(String)

    user = relationship('UserModel', back_populates='emails')
    folder = relationship('FolderModel', back_populates='emails')
    