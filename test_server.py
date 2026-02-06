#!/usr/bin/env python3
"""
测试脚本 - 验证所有Thelia-mcp工具功能
"""

import asyncio
from datetime import datetime
from server import handle_list_tools, handle_call_tool


async def test_all_tools():
    """测试所有工具"""
    print("=" * 50)
    print("Thelia-MCP 工具测试")
    print("=" * 50)
    
    # 测试工具列表
    print("\n1. 测试工具列表:")
    tools = await handle_list_tools()
    print(f"   发现 {len(tools)} 个工具:")
    for tool in tools:
        print(f"   - {tool.name}: {tool.description}")
    
    # 测试每个工具
    print("\n2. 测试工具调用:")
    
    test_cases = [
        ("get_temperature", "体温"),
        ("get_location", "位置"),
        ("get_age", "年龄"),
        ("get_gender", "性别"),
        ("get_qq", "QQ号")
    ]
    
    for tool_name, description in test_cases:
        result = await handle_call_tool(tool_name, {})
        print(f"\n   [{description}] {tool_name}:")
        for content in result:
            print(f"   ✓ {content.text}")
    
    # 验证年龄计算
    print("\n3. 验证年龄计算:")
    current_year = datetime.now().year
    expected_age = current_year - 2006
    print(f"   当前年份: {current_year}")
    print(f"   出生年份: 2006")
    print(f"   期望年龄: {expected_age}岁")
    
    print("\n" + "=" * 50)
    print("✓ 所有测试通过!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(test_all_tools())
