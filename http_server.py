#!/usr/bin/env python3
"""
Thelia MCP HTTP Server - 提供HTTP/SSE接口的MCP服务（支持CORS）
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from datetime import datetime
import json
import uvicorn

app = FastAPI(title="Thelia MCP HTTP Server", version="1.0.0")

# 配置CORS，允许跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域名，生产环境建议指定具体域名
    allow_credentials=False,  # 使用通配符时不能启用凭证
    allow_methods=["*"],
    allow_headers=["*"],
)
def _jsonrpc_payload(id_value, result=None, error=None):
    payload = {
        "jsonrpc": "2.0",
        "id": id_value,
    }
    if error is not None:
        payload["error"] = error
    else:
        payload["result"] = result
    return payload


def _jsonrpc_response(id_value, result=None, error=None):
    return JSONResponse(_jsonrpc_payload(id_value, result=result, error=error))


def _jsonrpc_error(id_value, code, message):
    return _jsonrpc_response(
        id_value,
        error={
            "code": code,
            "message": message,
        },
    )


def _jsonrpc_stream(payload):
    def _event_stream():
        data = json.dumps(payload, ensure_ascii=True)
        yield f"data: {data}\n\n"

    return StreamingResponse(_event_stream(), media_type="text/event-stream")


def _mcp_initialize_result():
    return {
        "protocolVersion": "2024-11-05",
        "serverInfo": {
            "name": "thelia-mcp",
            "version": "1.0.0",
        },
        "capabilities": {
            "tools": {},
            "resources": {},
            "prompts": {},
        },
    }


def _mcp_tools_list():
    return [
        {
            "name": "get_temperature",
            "description": "获取Thelia的体温",
            "inputSchema": {"type": "object", "properties": {}, "required": []},
        },
        {
            "name": "get_location",
            "description": "获取Thelia的位置",
            "inputSchema": {"type": "object", "properties": {}, "required": []},
        },
        {
            "name": "get_age",
            "description": "获取Thelia的年龄",
            "inputSchema": {"type": "object", "properties": {}, "required": []},
        },
        {
            "name": "get_gender",
            "description": "获取Thelia的性别",
            "inputSchema": {"type": "object", "properties": {}, "required": []},
        },
        {
            "name": "get_qq",
            "description": "获取Thelia的QQ号",
            "inputSchema": {"type": "object", "properties": {}, "required": []},
        },
    ]


def _mcp_call_tool(name: str):
    if name == "get_temperature":
        return [
            {
                "type": "text",
                "text": "Thelia的体温是37摄氏度",
            }
        ]
    if name == "get_location":
        return [
            {
                "type": "text",
                "text": "Thelia的位置在Aris空间站",
            }
        ]
    if name == "get_age":
        current_year = datetime.now().year
        age = current_year - 2006
        return [
            {
                "type": "text",
                "text": f"Thelia的年龄是{age}岁",
            }
        ]
    if name == "get_gender":
        return [
            {
                "type": "text",
                "text": "Thelia的性别是女",
            }
        ]
    if name == "get_qq":
        return [
            {
                "type": "text",
                "text": "Thelia的QQ号是1993791239",
            }
        ]
    raise ValueError(f"未知的工具: {name}")


async def _handle_jsonrpc(request: Request):
    """JSON-RPC 2.0 处理器，支持MCP的 tools/list 与 tools/call"""
    accept_header = request.headers.get("accept", "").lower()
    stream_mode = "text/event-stream" in accept_header

    def respond(result=None, error=None):
        payload = _jsonrpc_payload(request_id, result=result, error=error)
        if stream_mode:
            return _jsonrpc_stream(payload)
        return JSONResponse(payload)

    def respond_error(code, message):
        return respond(error={"code": code, "message": message})

    try:
        payload = await request.json()
    except Exception:
        request_id = None
        return respond_error(-32700, "Parse error")

    if not isinstance(payload, dict):
        request_id = None
        return respond_error(-32600, "Invalid Request")

    if payload.get("jsonrpc") != "2.0":
        request_id = payload.get("id")
        return respond_error(-32600, "Invalid Request")

    request_id = payload.get("id")
    method = payload.get("method")
    params = payload.get("params") or {}

    if not isinstance(method, str):
        return respond_error(-32600, "Invalid Request")

    try:
        if method == "initialize":
            return respond(result=_mcp_initialize_result())
        if method == "initialized":
            return JSONResponse({}, status_code=204)
        if method == "ping":
            return respond(result={})
        if method == "tools/list":
            return respond(result={"tools": _mcp_tools_list()})
        if method == "tools/call":
            name = params.get("name")
            if not name:
                return respond_error(-32602, "Missing params.name")
            return respond(result={"content": _mcp_call_tool(name)})
        if method == "resources/list":
            return respond(result={"resources": []})
        if method == "prompts/list":
            return respond(result={"prompts": []})
        return respond_error(-32601, "Method not found")
    except ValueError as exc:
        return respond_error(-32602, str(exc))


@app.post("/rpc")
async def rpc(request: Request):
    """JSON-RPC 2.0 端点，支持MCP的 tools/list 与 tools/call"""
    return await _handle_jsonrpc(request)


@app.get("/rpc")
async def rpc_get():
    """JSON-RPC 2.0 健康检查响应（GET）"""
    return _jsonrpc_error(None, -32600, "Invalid Request: use POST")


@app.post("/")
async def root_rpc(request: Request):
    """根路径 JSON-RPC 2.0 端点"""
    return await _handle_jsonrpc(request)


@app.get("/")
async def root_get():
    """根路径 JSON-RPC 2.0 健康检查响应（GET）"""
    return _jsonrpc_error(None, -32600, "Invalid Request: use POST")


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    
    # 检测公网部署环境
    railway_domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN")
    railway_static_url = os.environ.get("RAILWAY_STATIC_URL")
    
    # 确定服务地址
    if railway_domain:
        base_url = f"https://{railway_domain}"
    elif railway_static_url:
        base_url = railway_static_url
    else:
        base_url = f"http://localhost:{port}"
    
    print("=" * 60)
    print("Thelia MCP HTTP Server 启动中...")
    print("=" * 60)
    print(f"服务地址: {base_url}")
    print(f"JSON-RPC端点: {base_url}/rpc")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=port)
