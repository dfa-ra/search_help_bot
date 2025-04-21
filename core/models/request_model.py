from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, Boolean


@dataclass
class Request:
    __tablename__ = 'requests'

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, nullable=False)
    topic = Column(String, nullable=False)
    main_text = Column(String, nullable=False)
    executor_id = Column(Integer, nullable=False)
    is_open = Column(Boolean, nullable=False)
