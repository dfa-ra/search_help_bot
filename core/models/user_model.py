from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, BigInteger
from db.postgress.base import Base


@dataclass
class UserModel(Base):
    __tablename__ = 'users'

    telegram_id = Column(BigInteger, primary_key=True, index=True)
    name_tag = Column(String, nullable=False)
    name = Column(String, nullable=False)
    rating = Column(Integer, nullable=True)
    university = Column(String, nullable=True)
    course = Column(Integer, nullable=True)
    direction = Column(String, nullable=True)
