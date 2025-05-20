from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import hot_topics
from app.core.config import get_settings, clear_settings_cache
from app.core.scheduler import init_scheduler
from app.api import weather
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(funcName)s - %(message)s'
)

logger = logging.getLogger(__name__)

# 清除配置缓存并重新加载
clear_settings_cache()
settings = get_settings()

# 打印配置值进行调试
logger.debug(f"Settings: {settings.dict()}")

app = FastAPI(
    title="实时热搜资讯平台",
    description="提供知乎和微博的实时热搜数据",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 前端开发服务器地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(hot_topics.router, prefix="/api/v1", tags=["hot_topics"])
app.include_router(weather.router, prefix="/api/v1", tags=["weather"])

# 初始化调度器
scheduler = None

@app.on_event("startup")
async def startup_event():
    global scheduler
    scheduler = init_scheduler()

@app.on_event("shutdown")
async def shutdown_event():
    if scheduler:
        scheduler.shutdown()

@app.get("/")
async def root():
    return {"message": "Welcome to Hot News API"} 