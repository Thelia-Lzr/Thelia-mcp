#!/bin/bash
# Thelia-mcp 一键部署脚本

echo "========================================"
echo "Thelia-MCP 一键部署"
echo "========================================"

# 检查Python版本
echo "检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python 3。请先安装Python 3.8或更高版本。"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2 | cut -d '.' -f 1-2)
echo "Python版本: $PYTHON_VERSION"

# 安装依赖
echo ""
echo "安装依赖..."
pip install -r requirements.txt

# 选择运行模式
echo ""
echo "========================================"
echo "请选择运行模式:"
echo "1) MCP stdio 模式 (用于Claude Desktop等MCP客户端)"
echo "2) HTTP REST API 模式 (支持CORS，用于Web应用)"
echo "========================================"
read -p "请输入选项 (1 或 2): " choice

case $choice in
    1)
        echo ""
        echo "启动MCP stdio模式..."
        python3 server.py
        ;;
    2)
        echo ""
        echo "启动HTTP REST API模式..."
        echo "访问 http://localhost:8000 查看服务"
        echo "访问 http://localhost:8000/docs 查看API文档"
        python3 http_server.py
        ;;
    *)
        echo "无效的选项"
        exit 1
        ;;
esac
