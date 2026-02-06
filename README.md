# Thelia-mcp

一个基于Python的MCP（Model Context Protocol）服务，提供关于Thelia的信息查询工具。当前提供 HTTP JSON-RPC 2.0 接口（支持流式/SSE）。

## 功能

该服务提供以下5个工具：

1. **get_temperature** - 获取Thelia的体温（37摄氏度）
2. **get_location** - 获取Thelia的位置（Aris空间站）
3. **get_age** - 获取Thelia的年龄（当前年份 - 2006）
4. **get_gender** - 获取Thelia的性别（女）
5. **get_qq** - 获取Thelia的QQ号（1993791239）

## 一键部署

### 方法1：使用部署脚本（推荐）

**Linux/MacOS:**
```bash
./start.sh
```

**Windows:**
```cmd
start.bat
```

脚本会自动安装依赖并启动服务。

### 方法2：手动安装

#### 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方式

### 方式：HTTP JSON-RPC 2.0 模式（支持SSE）

```bash
python http_server.py
```

服务器将在 `http://localhost:8000` 启动HTTP服务。

#### JSON-RPC 2.0 端点

支持以下方法（MCP 常用方法已覆盖）：

- `initialize`
- `initialized`
- `ping`
- `tools/list`
- `tools/call`
- `resources/list`
- `prompts/list`

**端点：**
- `POST /` 或 `POST /rpc`（JSON-RPC 2.0）

**健康检查：**
- `GET /` 或 `GET /rpc` 会返回 JSON-RPC 错误（HTTP 200），用于平台健康检查。

#### JSON-RPC 示例

```bash
# 初始化
curl -X POST http://localhost:8000/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}'

# 列出工具
curl -X POST http://localhost:8000/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'

# 调用工具
curl -X POST http://localhost:8000/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_age"}}'
```

#### 流式（SSE）模式

当客户端发送 `Accept: text/event-stream` 时，服务会返回 SSE 流式响应：

```bash
curl -X POST http://localhost:8000/ \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"jsonrpc":"2.0","id":4,"method":"ping","params":{}}'
```

## 云平台部署

### Railway 一键部署

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/Thelia-Lzr/Thelia-mcp)

**手动部署到 Railway:**

1. 访问 [Railway](https://railway.app/)
2. 创建新项目，选择 "Deploy from GitHub repo"
3. 选择此仓库
4. Railway 会自动检测并部署 HTTP JSON-RPC 服务
5. 部署完成后，Railway 会提供一个公开的 URL

**Railway 配置说明:**
- 项目已包含 `Procfile`、`railway.toml` 和 `runtime.txt`
- 服务会自动使用 Railway 提供的 `PORT` 环境变量
- 支持自动健康检查和失败重启

**注意:** Railway 部署的是 HTTP JSON-RPC 2.0 模式。

### 其他云平台

本服务也可以部署到其他支持 Python 的云平台：

- **Heroku**: 包含 `Procfile`，可直接部署
- **Render**: 自动检测 Python 项目
- **Fly.io**: 需要创建 `fly.toml` 配置文件
- **Google Cloud Run**: 需要 Dockerfile（可自行添加）

## MCP 客户端连接提示

请确保客户端使用 HTTP JSON-RPC 2.0（可选 SSE）。如果客户端默认使用 stdio 或 WebSocket，需要改成 HTTP 传输方式。

## 工具使用示例

当服务器连接到MCP客户端后，可以调用以下工具：

- `get_temperature` - 返回: "Thelia的体温是37摄氏度"
- `get_location` - 返回: "Thelia的位置在Aris空间站"
- `get_age` - 返回: "Thelia的年龄是X岁（当前年份 - 2006）"
- `get_gender` - 返回: "Thelia的性别是女"
- `get_qq` - 返回: "Thelia的QQ号是1993791239"

## 测试

运行测试脚本验证所有工具：

```bash
python test_server.py
```

## 技术栈

- Python 3.8+
- FastAPI + Uvicorn - HTTP JSON-RPC 2.0
- SSE 流式响应支持
- CORS 支持

## 开发

### 项目结构

```
Thelia-mcp/
├── server.py          # MCP stdio服务器（可选，本地使用）
├── http_server.py     # HTTP JSON-RPC 2.0 服务器（支持SSE）
├── test_server.py     # 测试脚本
├── start.sh           # Linux/MacOS部署脚本
├── start.bat          # Windows部署脚本
├── Procfile           # Railway/Heroku部署配置
├── railway.toml       # Railway平台配置
├── runtime.txt        # Python版本指定
├── requirements.txt   # Python依赖
├── .gitignore        # Git忽略文件
└── README.md         # 项目说明
```

### 扩展功能

要添加新的工具：

**对于 HTTP JSON-RPC 模式** (http_server.py):
1. 在 `_mcp_tools_list()` 中添加工具定义
2. 在 `_mcp_call_tool()` 中添加工具处理逻辑

## 许可证

本项目仅供学习和实验使用。
