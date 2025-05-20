import aiohttp
from bs4 import BeautifulSoup
from app.core.config import get_settings
from typing import List, Dict, Any
import logging
import re
import inspect

# 配置日志格式
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(funcName)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

class ZhihuCrawler:
    def __init__(self):
        self.settings = get_settings()
        self.headers = {
            "User-Agent": self.settings.USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate",  # 移除 br 编码
            "Connection": "keep-alive",
            "Cookie": self.settings.ZHIHU_COOKIE or "",
            "Referer": "https://www.zhihu.com/",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1"
        }
        self.url = self.settings.ZHIHU_HOT_URL
        logger.info(f"知乎爬虫初始化完成，URL: {self.url}")
        if not self.settings.ZHIHU_COOKIE:
            logger.warning("知乎Cookie未设置，可能无法获取热搜数据")

    def extract_question_id(self, url: str) -> str:
        """从URL中提取问题ID"""
        question_pattern = r'/question/(\d+)'
        match = re.search(question_pattern, url)
        if match:
            return match.group(1)
        return ""

    async def check_cookie_valid(self, session: aiohttp.ClientSession) -> bool:
        """检查cookie是否有效"""
        try:
            async with session.get("https://www.zhihu.com/", headers=self.headers) as response:
                if response.status != 200:
                    logger.error(f"检查Cookie有效性时出错: HTTP {response.status}")
                    return False
                    
                html = await response.text()
                # 如果页面包含登录按钮，说明cookie已失效
                if "登录" in html and "注册" in html:
                    logger.error("知乎Cookie已失效，请更新Cookie")
                    return False
                return True
        except Exception as e:
            logger.error(f"检查Cookie有效性时出错: {str(e)}", exc_info=True)
            return False

    async def fetch_hot_topics(self) -> List[Dict[str, Any]]:
        """获取知乎热搜话题"""
        try:
            logger.info("开始获取知乎热搜...")
            async with aiohttp.ClientSession() as session:
                # 首先检查cookie是否有效
                if not await self.check_cookie_valid(session):
                    return []

                async with session.get(self.url, headers=self.headers) as response:
                    if response.status != 200:
                        logger.error(f"获取知乎热搜失败: HTTP {response.status}")
                        return []
                        
                    html = await response.text()
                    logger.info(f"知乎响应状态码: {response.status}")
                    logger.debug(f"知乎响应内容: {html[:500]}...")
                    
                    # 检查是否需要登录
                    if "登录" in html and "注册" in html:
                        logger.error("知乎Cookie已失效，请更新Cookie")
                        return []
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # 调试信息：打印所有可能的类名
            all_classes = set()
            for tag in soup.find_all(class_=True):
                all_classes.update(tag['class'])
            logger.info(f"页面中所有的类名: {all_classes}")
            
            # 尝试不同的选择器
            items = soup.select('.HotList-item')
            if not items:
                items = soup.select('.HotItem')
            if not items:
                items = soup.select('[data-zop-itemid]')
            if not items:
                items = soup.select('.HotList-item')
            
            logger.info(f"找到热搜条目数: {len(items)}")
            
            hot_topics = []
            for index, item in enumerate(items, 1):
                # 打印每个item的HTML结构，用于调试
                logger.debug(f"Item {index} HTML: {item}")
                
                # 尝试不同的标题选择器
                title_element = (
                    item.select_one('.HotList-itemTitle') or 
                    item.select_one('.HotItem-title') or
                    item.select_one('.HotItem-content') or
                    item.select_one('a')
                )
                
                if title_element:
                    # 打印找到的标题元素，用于调试
                    logger.debug(f"Title element found: {title_element}")
                    logger.debug(f"Title element attrs: {title_element.attrs}")
                    logger.debug(f"Title element parent: {title_element.parent}")
                    
                    # 获取链接
                    href = title_element.get('href', '')
                    logger.debug(f"Original href: {href}")
                    
                    # 如果href为空，尝试从父元素获取
                    if not href and title_element.parent:
                        href = title_element.parent.get('href', '')
                        logger.debug(f"Parent href: {href}")
                    
                    # 确保链接是完整的问题链接
                    if href.startswith('/'):
                        href = f"https://www.zhihu.com{href}"
                    
                    # 提取问题ID并构建标准问题链接
                    question_id = self.extract_question_id(href)
                    if question_id:
                        href = f"https://www.zhihu.com/question/{question_id}"
                    
                    logger.debug(f"Final href: {href}")
                    
                    # 获取热度值
                    hot_value = ""
                    metrics_element = (
                        item.select_one('.HotList-itemMetrics') or 
                        item.select_one('.HotItem-metrics') or
                        item.select_one('.HotItem-meta')
                    )
                    if metrics_element:
                        hot_value = metrics_element.text.strip()
                    
                    hot_topic = {
                        "title": title_element.text.strip(),
                        "url": href,
                        "source": "zhihu",
                        "rank": index,
                        "hot_value": hot_value
                    }
                    hot_topics.append(hot_topic)
                    logger.debug(f"已添加热搜: {hot_topic['title']} - {hot_topic['url']}")
            
            logger.info(f"成功获取知乎热搜 {len(hot_topics)} 条")
            return hot_topics
        except Exception as e:
            logger.error(f"知乎热搜爬取失败: {str(e)}", exc_info=True)
            return []