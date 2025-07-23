#!/bin/bash
# 文档问答系统启动脚本

set -e

echo "正在启动文档问答系统..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未安装Python3"
    exit 1
fi



# 杀死之前的uvicorn进程（强制）
echo "检查并关闭已有的uvicorn进程..."
pids=$(pgrep -f "uvicorn main:app" || true)
if [ -n "$pids" ]; then
    echo "发现uvicorn进程: $pids，正在强制关闭..."
    kill -9 $pids 2>/dev/null || true
    # 等待进程完全退出
    while pgrep -f "uvicorn main:app" > /dev/null; do
        sleep 1
    done
    echo "uvicorn进程已关闭。"
else
    echo "未发现正在运行的uvicorn进程。"
fi


# 安装依赖
echo "安装Python依赖..."
pip3 install -r requirements.txt

# 初始化数据库
echo "初始化数据库..."
python init_db.py

# 启动服务器
echo "启动服务器..."
if command -v uvicorn &> /dev/null; then
    uvicorn main:app --host ${HOST:-127.0.0.1} --port ${PORT:-8000} --reload
else
    python3 -m uvicorn main:app --host ${HOST:-127.0.0.1} --port ${PORT:-8000} --reload
fi
