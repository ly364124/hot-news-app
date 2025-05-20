from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
from app.core.database import Base

class HotTopic(Base):
    __tablename__ = "hot_topics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    url = Column(String(512), nullable=False)
    source = Column(Enum('zhihu', 'weibo'), nullable=False)
    rank = Column(Integer, nullable=False)
    hot_value = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 