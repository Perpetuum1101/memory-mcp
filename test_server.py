"""Simple test script for the MCP server."""

import asyncio
from src.memory_mcp.server import handle_call_tool, handle_list_tools


async def test_memory_functions():
    """Test the memory functions."""
    print("Testing MCP server tools...")
    
    # Test list tools
    tools = await handle_list_tools()
    print(f"Available tools: {[tool.name for tool in tools]}")
    
    # Test save_memory
    save_result = await handle_call_tool("save_memory", {"key": "test_key", "value": "test_value"})
    print(f"Save result: {save_result[0].text}")
    
    # Test get_memory
    get_result = await handle_call_tool("get_memory", {"key": "test_key"})
    print(f"Get result: {get_result[0].text}")
    
    # Test get_memory for non-existent key
    get_missing = await handle_call_tool("get_memory", {"key": "missing_key"})
    print(f"Missing key result: {get_missing[0].text}")
    
    print("All tests completed!")


if __name__ == "__main__":
    asyncio.run(test_memory_functions())