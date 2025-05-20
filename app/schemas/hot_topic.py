from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class HotTopicBase(BaseModel):
    title: str
    url: str
    source: str
    rank: int
    hot_value: Optional[str] = None

class HotTopicCreate(HotTopicBase):
    pass

class HotTopicResponse(HotTopicBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 