from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.crawlers.zhihu_crawler import ZhihuCrawler
from app.crawlers.weibo_crawler import WeiboCrawler
from app.core.database import SessionLocal
from app.models.hot_topic import HotTopic
from datetime import datetime
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

async def crawl_topics():
    """异步抓取热搜话题"""
    try:
        # 创建爬虫实例
        zhihu_crawler = ZhihuCrawler()
        weibo_crawler = WeiboCrawler()
        
        # 获取热搜话题
        zhihu_topics = await zhihu_crawler.fetch_hot_topics()
        weibo_topics = await weibo_crawler.fetch_hot_topics()
        
        return zhihu_topics, weibo_topics
    except Exception as e:
        logger.error(f"抓取热搜话题失败：{str(e)}")
        return [], []

def save_topics(zhihu_topics, weibo_topics):
    """保存热搜话题到数据库"""
    db = SessionLocal()
    try:
        # 清空旧数据
        db.query(HotTopic).delete()
        
        # 保存知乎话题
        for topic in zhihu_topics:
            db_topic = HotTopic(
                title=topic['title'],
                url=topic['url'],
                source='zhihu',
                rank=topic['rank'],
                hot_value=topic.get('hot_value', '')
            )
            db.add(db_topic)
        
        # 保存微博话题
        for topic in weibo_topics:
            db_topic = HotTopic(
                title=topic['title'],
                url=topic['url'],
                source='weibo',
                rank=topic['rank'],
                hot_value=topic.get('hot_value', '')
            )
            db.add(db_topic)
        
        db.commit()
        logger.info(f"成功更新热搜话题，知乎：{len(zhihu_topics)}条，微博：{len(weibo_topics)}条")
    except Exception as e:
        db.rollback()
        logger.error(f"保存热搜话题失败：{str(e)}")
        raise
    finally:
        db.close()

def crawl_and_save_topics():
    """抓取并保存热搜话题"""
    try:
        # 创建事件循环
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # 运行异步抓取
        zhihu_topics, weibo_topics = loop.run_until_complete(crawl_topics())
        
        # 保存到数据库
        save_topics(zhihu_topics, weibo_topics)
        
        # 关闭事件循环
        loop.close()
    except Exception as e:
        logger.error(f"抓取热搜话题失败：{str(e)}")

def init_scheduler():
    """初始化调度器"""
    scheduler = BackgroundScheduler()
    
    # 立即执行一次
    scheduler.add_job(crawl_and_save_topics, 'date', run_date=datetime.now())
    
    # 每30分钟执行一次
    scheduler.add_job(
        crawl_and_save_topics,
        IntervalTrigger(minutes=30),
        id='crawl_hot_topics',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("热搜话题抓取任务已启动")
    return scheduler 