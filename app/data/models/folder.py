from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class FolderModel(Base):
    __tablename__ = 'folder'

    folder_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.user_id'))
    name: Mapped[str] = mapped_column(String)
    
    user = relationship('UserModel', back_populates='folders')
    emails = relationship('EmailModel', back_populates='folder')