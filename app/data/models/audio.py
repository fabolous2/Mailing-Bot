from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class AudioModel(Base):
    __tablename__ = 'email'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.user_id'))
    audio: Mapped[str] = mapped_column(String, unique=True)

    user = relationship('UserModel', back_populates='audios')
    