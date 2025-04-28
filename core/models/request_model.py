from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, Boolean, BigInteger

from db.postgress.base import Base


@dataclass
class RequestModel(Base):
    __tablename__ = 'requests'

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(BigInteger, nullable=False)
    executor_id = Column(BigInteger, nullable=True)

    topic = Column(String, nullable=False)
    main_text = Column(String, nullable=False)
    deadline = Column(String, nullable=False)
    money = Column(Integer, nullable=False)
    is_open = Column(Boolean, nullable=False)
    is_complete = Column(Boolean, nullable=False)

    file_id = Column(String, nullable=True)

