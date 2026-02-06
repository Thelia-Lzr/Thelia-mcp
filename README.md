# Thelia-mcp

一个基于Python的MCP（Model Context Protocol）服务，提供关于Thelia的信息查询工具。支持两种模式：标准MCP stdio协议和HTTP REST API（支持CORS跨域访问）。

## 功能

该服务提供以下5个工具：

1. **get_temperature** - 获取Thelia的体温（37摄氏度）
2. **get_location** - 获取Thelia的位置（Aris空间站）
3. **get_age** - 获取Thelia的年龄（当前年份 - 2006）
4. **get_gender** - 获取Thelia的性别（女）
5. **get_qq** - 获取Thelia的QQ号（1993791239）

## 一键部署

### 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方式

### 方式1：MCP stdio模式（用于MCP客户端）

```bash
python server.py
```

服务器将通过标准输入输出（stdio）与MCP客户端通信。

### 方式2：HTTP REST API模式（支持CORS跨域）

```bash
python http_server.py
```

服务器将在 `http://localhost:8000` 启动HTTP服务，支持跨域访问。

访问 http://localhost:8000/docs 查看交互式API文档。

#### HTTP API端点

- `GET /` - 服务信息
- `GET /tools` - 列出所有工具
- `GET /api/temperature` - 获取体温
- `GET /api/location` - 获取位置
- `GET /api/age` - 获取年龄
- `GET /api/gender` - 获取性别
- `GET /api/qq` - 获取QQ号

#### HTTP API示例

```bash
# 获取所有工具
curl http://localhost:8000/tools

# 获取体温
curl http://localhost:8000/api/temperature

# 获取年龄
curl http://localhost:8000/api/age
```

## 配置到MCP客户端

### Claude Desktop 配置

在 Claude Desktop 的配置文件中添加：

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "thelia": {
      "command": "python",
      "args": ["/path/to/Thelia-mcp/server.py"]
    }
  }
}
```

请将 `/path/to/Thelia-mcp/server.py` 替换为实际的文件路径。

### 其他MCP客户端

该服务器使用标准的MCP stdio传输协议，兼容所有支持MCP的客户端。

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
- MCP (Model Context Protocol) SDK - stdio模式
- FastAPI + Uvicorn - HTTP REST API模式
- CORS支持 - 允许跨域访问

## 开发

### 项目结构

```
Thelia-mcp/
├── server.py          # MCP stdio服务器
├── http_server.py     # HTTP REST API服务器（支持CORS）
├── test_server.py     # 测试脚本
├── requirements.txt   # Python依赖
├── .gitignore        # Git忽略文件
└── README.md         # 项目说明
```

### 扩展功能

要添加新的工具：

**对于 stdio 模式** (server.py):
1. 在 `handle_list_tools()` 函数中添加新的工具定义
2. 在 `handle_call_tool()` 函数中添加新的工具处理逻辑

**对于 HTTP 模式** (http_server.py):
1. 在 `list_tools()` 函数中添加工具信息
2. 创建新的API端点处理函数

## 许可证

本项目仅供学习和实验使用。
