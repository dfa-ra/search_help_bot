from dataclasses import dataclass

from sqlalchemy import Column, Integer, String
from db.base import Base


@dataclass
class User(Base):
    __tablename__ = 'users'

    telegram_id = Column(Integer, primary_key=True, index=True)
    name_tag = Column(String, nullable=False)
    name = Column(String, nullable=False)
    university = Column(String, nullable=True)
    course = Column(Integer, nullable=True)
    direction = Column(String, nullable=True)
