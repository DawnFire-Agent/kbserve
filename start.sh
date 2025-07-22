#!/bin/bash
# 文档问答系统启动脚本

set -e

echo "正在启动文档问答系统..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未安装Python3"
    exit 1
fi

# 安装依赖
echo "安装Python依赖..."
pip install -r requirements.txt

# 初始化数据库
echo "初始化数据库..."
python init_db.py

# 启动服务器
echo "启动服务器..."
uvicorn main:app --host ${HOST:-127.0.0.1} --port ${PORT:-8000} --reload
