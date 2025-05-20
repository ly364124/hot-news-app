from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.hot_topic import HotTopic
from app.core.database import get_db
from app.schemas.hot_topic import HotTopicResponse

router = APIRouter()

@router.get("/hot-topics", response_model=List[HotTopicResponse])
async def get_hot_topics(
    source: str = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    获取热搜话题列表
    - source: 可选，来源（zhihu/weibo）
    - limit: 可选，返回数量限制
    """
    query = db.query(HotTopic)
    if source:
        query = query.filter(HotTopic.source == source)
    
    topics = query.order_by(HotTopic.rank).limit(limit).all()
    return topics

@router.get("/hot-topics/{source}", response_model=List[HotTopicResponse])
async def get_hot_topics_by_source(
    source: str,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    获取指定来源的热搜话题
    - source: 来源（zhihu/weibo）
    - limit: 可选，返回数量限制
    """
    if source not in ['zhihu', 'weibo']:
        raise HTTPException(status_code=400, detail="Invalid source")
    
    topics = db.query(HotTopic)\
        .filter(HotTopic.source == source)\
        .order_by(HotTopic.rank)\
        .limit(limit)\
        .all()
    return topics 