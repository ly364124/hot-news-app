import pymysql
from app.core.config import get_settings

def init_database():
    settings = get_settings()
    
    # 解析数据库URL
    db_url = settings.DATABASE_URL
    # 移除 mysql+pymysql:// 前缀
    db_url = db_url.replace('mysql+pymysql://', '')
    # 分割用户名、密码和主机
    user_pass, host_db = db_url.split('@')
    user, password = user_pass.split(':')
    host, db = host_db.split('/')
    
    try:
        # 首先连接到MySQL服务器（不指定数据库）
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password
        )
        
        with conn.cursor() as cursor:
            # 读取SQL文件
            with open('init.sql', 'r', encoding='utf-8') as f:
                sql_commands = f.read()
            
            # 执行SQL命令
            for command in sql_commands.split(';'):
                if command.strip():
                    cursor.execute(command)
            
            conn.commit()
            print("数据库初始化成功！")
            
    except Exception as e:
        print(f"数据库初始化失败：{str(e)}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    init_database() 