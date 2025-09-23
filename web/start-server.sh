#!/bin/bash

# 论文生成系统 - 启动脚本

echo "📄 论文生成系统 Web界面"
echo "========================="

# 检查端口是否被占用
PORT=8080
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  端口 $PORT 已被占用，尝试其他端口..."
    PORT=8081
fi

echo "🚀 启动Web服务器..."
echo "📍 地址: http://localhost:$PORT"
echo "⏹️  按 Ctrl+C 停止服务器"
echo ""

# 尝试不同的服务器
if command -v python3 &> /dev/null; then
    echo "使用 Python3 服务器"
    python3 -m http.server $PORT
elif command -v python &> /dev/null; then
    echo "使用 Python 服务器"
    python -m http.server $PORT
elif command -v npx &> /dev/null; then
    echo "使用 Node.js 服务器"
    npx http-server -p $PORT -c-1
else
    echo "❌ 未找到可用的服务器"
    echo "请安装 Python 或 Node.js"
    echo ""
    echo "安装方法："
    echo "- Python: https://python.org/downloads/"
    echo "- Node.js: https://nodejs.org/downloads/"
    exit 1
fi