from typing import Optional, Dict, Any
from pydantic_settings import BaseSettings
from pydantic import Field, validator
from functools import lru_cache
import os
from pathlib import Path

class DatabaseSettings(BaseSettings):
    """数据库配置"""
    DATABASE_URL: str = Field(
        default="mysql+pymysql://root:password@localhost/hot_news",
        description="数据库连接URL"
    )

class CrawlerSettings(BaseSettings):
    """爬虫配置"""
    ZHIHU_HOT_URL: str = Field(
        default="https://www.zhihu.com/hot",
        description="知乎热搜URL"
    )
    WEIBO_HOT_URL: str = Field(
        default="https://s.weibo.com/top/summary",
        description="微博热搜URL"
    )
    CRAWL_INTERVAL: int = Field(
        default=30,
        description="爬虫更新间隔（分钟）",
        ge=1  # 确保间隔大于等于1分钟
    )
    USER_AGENT: str = Field(
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        description="用户代理"
    )
    ZHIHU_COOKIE: str = Field(
        default="",
        description="知乎Cookie"
    )

    @validator('CRAWL_INTERVAL')
    def validate_crawl_interval(cls, v: int) -> int:
        """验证爬虫更新间隔"""
        if v < 30:
            raise ValueError("爬虫更新间隔必须大于等于30分钟")
        return v

class Settings(BaseSettings):
    """应用配置"""
    # 环境
    ENV: str = Field(
        default="development",
        description="运行环境"
    )
    
    # 数据库配置
    DATABASE_URL: str = Field(
        default="mysql+pymysql://root:password@localhost/hot_news",
        description="数据库连接URL"
    )
    
    # 知乎配置
    ZHIHU_USERNAME: str
    ZHIHU_PASSWORD: str
    ZHIHU_HOT_URL: str = "https://www.zhihu.com/hot"
    ZHIHU_COOKIE: Optional[str] = None

    # 微博配置
    WEIBO_HOT_URL: str = "https://s.weibo.com/top/summary"

    # 爬虫配置
    CRAWL_INTERVAL: int = Field(
        default=30,
        description="爬虫更新间隔（分钟）"
    )
    USER_AGENT: str = Field(
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        description="用户代理"
    )

    # 和风天气配置
    QWEATHER_API_KEY: str = Field(
        default="",
        description="和风天气API密钥"
    )

    # 高德地图配置
    AMAP_KEY: str = Field(
        default="",
        description="高德地图API密钥"
    )

    # API基础URL配置
    API_BASE_URL: str = Field(
        default="http://localhost:8000",
        description="API基础URL"
    )

    class Config:
        env_file = ".env.development"
        env_file_encoding = 'utf-8'
        case_sensitive = True

    def dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "database_url": self.DATABASE_URL,
            "zhihu_hot_url": self.ZHIHU_HOT_URL,
            "weibo_hot_url": self.WEIBO_HOT_URL,
            "crawl_interval": self.CRAWL_INTERVAL,
            "user_agent": self.USER_AGENT,
            "zhihu_cookie": self.ZHIHU_COOKIE,
            "env": self.ENV,
            "qweather_api_key": self.QWEATHER_API_KEY,
            "amap_key": self.AMAP_KEY
        }

@lru_cache()
def get_settings() -> Settings:
    """
    获取配置实例，使用缓存避免重复读取
    """
    # print("Loading settings...")
    # print("Current working directory:", os.getcwd())
    # print("ENV file exists:", os.path.exists(".envDev"))
    # if os.path.exists(".envDev"):
    #     with open(".envDev", "r", encoding="utf-8") as f:
    #         print("ENV file contents:")
    #         print(f.read())
    return Settings()

def clear_settings_cache():
    """
    清除配置缓存
    """
    get_settings.cache_clear()
    global settings
    settings = get_settings()  # 重新加载配置

# 全局配置实例
settings = get_settings() 

# console.log(import.meta.env);