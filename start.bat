@echo off
REM Thelia-mcp 一键部署脚本 (Windows)

echo ========================================
echo Thelia-MCP 一键部署
echo ========================================

REM 检查Python
echo 检查Python环境...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo 错误: 未找到Python。请先安装Python 3.8或更高版本。
    pause
    exit /b 1
)

python --version

REM 安装依赖
echo.
echo 安装依赖...
pip install -r requirements.txt

REM 选择运行模式
echo.
echo ========================================
echo 请选择运行模式:
echo 1) MCP stdio 模式 (用于Claude Desktop等MCP客户端)
echo 2) HTTP REST API 模式 (支持CORS，用于Web应用)
echo ========================================
set /p choice=请输入选项 (1 或 2): 

if "%choice%"=="1" (
    echo.
    echo 启动MCP stdio模式...
    python server.py
) else if "%choice%"=="2" (
    echo.
    echo 启动HTTP REST API模式...
    echo 访问 http://localhost:8000 查看服务
    echo 访问 http://localhost:8000/docs 查看API文档
    python http_server.py
) else (
    echo 无效的选项
    pause
    exit /b 1
)

pause
