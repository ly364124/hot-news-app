from app.core.database import Base, engine
from app.models.hot_topic import HotTopic

def init_db():
    """初始化数据库，创建所有表"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db() 