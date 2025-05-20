import aiohttp
from bs4 import BeautifulSoup
from app.core.config import get_settings
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class WeiboCrawler:
    def __init__(self):
        self.settings = get_settings()
        self.headers = {
            "User-Agent": self.settings.USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }
        self.url = self.settings.WEIBO_HOT_URL
        logger.info(f"微博爬虫初始化完成，URL: {self.url}")

    async def fetch_hot_topics(self) -> List[Dict[str, Any]]:
        """获取微博热搜话题"""
        try:
            logger.info("开始获取微博热搜...")
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, headers=self.headers) as response:
                    # 使用gb2312编码解码响应内容
                    html = await response.text(encoding='gb2312')
                    logger.info(f"微博响应状态码: {response.status}")
                    logger.debug(f"微博响应内容: {html[:500]}...")
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # 调试信息：打印所有可能的类名
            all_classes = set()
            for tag in soup.find_all(class_=True):
                all_classes.update(tag['class'])
            # logger.info(f"页面中所有的类名: {all_classes}")
            
            # 获取热搜列表
            items = soup.select('.td-02')
            logger.info(f"找到热搜条目数: {len(items)}")
            
            hot_topics = []
            for index, item in enumerate(items, 1):
                # 打印每个item的HTML结构，用于调试
                logger.debug(f"Item {index} HTML: {item}")
                
                # 获取标题和链接
                title_element = item.select_one('a')
                if title_element:
                    # 打印找到的标题元素，用于调试
                    logger.debug(f"Title element found: {title_element}")
                    logger.debug(f"Title element attrs: {title_element.attrs}")
                    
                    # 获取链接
                    href = title_element.get('href', '')
                    if href.startswith('/'):
                        href = f"https://s.weibo.com{href}"
                    
                    # 获取热度值
                    hot_value = ""
                    hot_element = item.select_one('.td-03')
                    if hot_element:
                        hot_value = hot_element.text.strip()
                    
                    hot_topic = {
                        "title": title_element.text.strip(),
                        "url": href,
                        "source": "weibo",
                        "rank": index,
                        "hot_value": hot_value
                    }
                    hot_topics.append(hot_topic)
                    logger.debug(f"已添加热搜: {hot_topic['title']} - {hot_topic['url']}")
            
            logger.info(f"成功获取微博热搜 {len(hot_topics)} 条")
            return hot_topics
        except Exception as e:
            logger.error(f"微博热搜爬取失败: {str(e)}", exc_info=True)
            return [] 