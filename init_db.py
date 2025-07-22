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
    TORTOISE_ORM = {
        "connections": {
            "default": os.getenv("DATABASE_URL", "sqlite://db.sqlite3")
        },
        "apps": {
            "models": {
                "models": ["models.document", "models.chunk"],
                "default_connection": "default",
            },
        },
    }
    
    # 初始化Tortoise ORM
    await Tortoise.init(config=TORTOISE_ORM)
    
    # 创建表
    await Tortoise.generate_schemas()
    
    print("数据库初始化完成!")
    
    # 关闭连接
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(init_db())
