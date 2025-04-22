from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, Boolean

from db.base import Base


@dataclass
class Request(Base):
    __tablename__ = 'requests'

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, nullable=False)
    executor_id = Column(Integer, nullable=True)

    topic = Column(String, nullable=False)
    main_text = Column(String, nullable=False)
    deadline = Column(String, nullable=False)
    money = Column(Integer, nullable=False)
    is_open = Column(Boolean, nullable=False)

