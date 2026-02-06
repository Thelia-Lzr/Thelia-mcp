#!/usr/bin/env python3
"""
Thelia MCP HTTP Server - 提供HTTP/SSE接口的MCP服务（支持CORS）
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import uvicorn

app = FastAPI(title="Thelia MCP HTTP Server", version="1.0.0")

# 配置CORS，允许跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域名，生产环境建议指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """根路径，返回服务信息"""
    return {
        "name": "Thelia MCP Server",
        "version": "1.0.0",
        "description": "提供关于Thelia的信息查询服务",
        "endpoints": {
            "tools": "/tools - 列出所有可用工具",
            "temperature": "/api/temperature - 获取体温",
            "location": "/api/location - 获取位置",
            "age": "/api/age - 获取年龄",
            "gender": "/api/gender - 获取性别",
            "qq": "/api/qq - 获取QQ号"
        }
    }


@app.get("/tools")
async def list_tools():
    """列出所有可用的工具"""
    return {
        "tools": [
            {
                "name": "get_temperature",
                "description": "获取Thelia的体温",
                "endpoint": "/api/temperature"
            },
            {
                "name": "get_location",
                "description": "获取Thelia的位置",
                "endpoint": "/api/location"
            },
            {
                "name": "get_age",
                "description": "获取Thelia的年龄",
                "endpoint": "/api/age"
            },
            {
                "name": "get_gender",
                "description": "获取Thelia的性别",
                "endpoint": "/api/gender"
            },
            {
                "name": "get_qq",
                "description": "获取Thelia的QQ号",
                "endpoint": "/api/qq"
            }
        ]
    }


@app.get("/api/temperature")
async def get_temperature():
    """获取Thelia的体温"""
    return {
        "tool": "get_temperature",
        "result": "Thelia的体温是37摄氏度",
        "data": {
            "temperature": 37,
            "unit": "摄氏度"
        }
    }


@app.get("/api/location")
async def get_location():
    """获取Thelia的位置"""
    return {
        "tool": "get_location",
        "result": "Thelia的位置在Aris空间站",
        "data": {
            "location": "Aris空间站"
        }
    }


@app.get("/api/age")
async def get_age():
    """获取Thelia的年龄"""
    current_year = datetime.now().year
    age = current_year - 2006
    return {
        "tool": "get_age",
        "result": f"Thelia的年龄是{age}岁（{current_year} - 2006）",
        "data": {
            "age": age,
            "birth_year": 2006,
            "current_year": current_year
        }
    }


@app.get("/api/gender")
async def get_gender():
    """获取Thelia的性别"""
    return {
        "tool": "get_gender",
        "result": "Thelia的性别是女",
        "data": {
            "gender": "女"
        }
    }


@app.get("/api/qq")
async def get_qq():
    """获取Thelia的QQ号"""
    return {
        "tool": "get_qq",
        "result": "Thelia的QQ号是1993791239",
        "data": {
            "qq": "1993791239"
        }
    }


if __name__ == "__main__":
    print("=" * 60)
    print("Thelia MCP HTTP Server 启动中...")
    print("=" * 60)
    print("服务地址: http://localhost:8000")
    print("API文档: http://localhost:8000/docs")
    print("工具列表: http://localhost:8000/tools")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000)
