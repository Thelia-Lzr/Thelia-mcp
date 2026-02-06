#!/usr/bin/env python3
"""
Thelia MCP Server - 提供关于Thelia的信息服务
"""

import asyncio
from datetime import datetime
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio


# 创建MCP服务器实例
server = Server("thelia-mcp")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    列出所有可用的工具
    """
    return [
        types.Tool(
            name="get_temperature",
            description="获取Thelia的体温",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="get_location",
            description="获取Thelia的位置",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="get_age",
            description="获取Thelia的年龄",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="get_gender",
            description="获取Thelia的性别",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="get_qq",
            description="获取Thelia的QQ号",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    处理工具调用请求
    """
    if name == "get_temperature":
        return [
            types.TextContent(
                type="text",
                text="Thelia的体温是37摄氏度"
            )
        ]
    elif name == "get_location":
        return [
            types.TextContent(
                type="text",
                text="Thelia的位置在Aris空间站"
            )
        ]
    elif name == "get_age":
        current_year = datetime.now().year
        age = current_year - 2006
        return [
            types.TextContent(
                type="text",
                text=f"Thelia的年龄是{age}岁（{current_year} - 2006）"
            )
        ]
    elif name == "get_gender":
        return [
            types.TextContent(
                type="text",
                text="Thelia的性别是女"
            )
        ]
    elif name == "get_qq":
        return [
            types.TextContent(
                type="text",
                text="Thelia的QQ号是1993791239"
            )
        ]
    else:
        raise ValueError(f"未知的工具: {name}")


async def main():
    """
    主函数：运行MCP服务器
    """
    # 使用stdio传输运行服务器
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="thelia-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
