from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class UserModel(Base):
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gmail: Mapped[Optional[str]] = mapped_column(String, nullable=True, unique=True)
    password: Mapped[Optional[str]] = mapped_column(String(16), nullable=True, unique=True)
    