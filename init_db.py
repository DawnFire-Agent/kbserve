#!/usr/bin/env python3
"""
数据库初始化脚本
运行此脚本来初始化数据库和表结构
"""

import asyncio
from tortoise import Tortoise
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

async def init_db():
    """初始化数据库"""
    # 数据库配置
    # MySQL 配置 - 默认启用
    TORTOISE_ORM = {
        "connections": {
            "default": os.getenv(
                "DATABASE_URL",
                "mysql://root:p1ssw0rd@127.0.0.1:3306/dawnfire_db"
            )
        },
        "apps": {
            "models": {
                "models": ["models.document", "models.chunk"],
                "default_connection": "default",
            },
        },
    }

    # 如果需要使用 SQLite，请设置环境变量 DATABASE_URL=sqlite://db.sqlite3
    # 或者直接修改上面的默认连接字符串
    
    try:
        # 初始化Tortoise ORM
        await Tortoise.init(config=TORTOISE_ORM)
        
        # 创建表
        await Tortoise.generate_schemas()
        
        print("数据库初始化完成!")
        
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        print("请确保:")
        print("1. MySQL 服务已启动")
        print("2. 数据库 'dawnfire_db' 已创建")
        print("3. 用户名和密码正确")
        print("4. 已安装 aiomysql 驱动: pip install aiomysql")
        raise
    finally:
        # 关闭连接
        await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(init_db())
