"""Memory MCP server implementation."""

import asyncio
import logging
from typing import Any, Dict, Optional

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


# In-memory storage for simplicity
memory_store: Dict[str, str] = {}

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create server instance
server = Server("memory-mcp")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="get_memory",
            description="Retrieve stored memory by key",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "The key to retrieve memory for"
                    }
                },
                "required": ["key"]
            }
        ),
        Tool(
            name="save_memory",
            description="Save memory with a key",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "The key to store memory under"
                    },
                    "value": {
                        "type": "string", 
                        "description": "The memory content to store"
                    }
                },
                "required": ["key", "value"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    
    if name == "get_memory":
        key = arguments.get("key")
        if not key:
            return [TextContent(type="text", text="Error: key parameter is required")]
        
        value = memory_store.get(key)
        if value is None:
            return [TextContent(type="text", text=f"No memory found for key: {key}")]
        
        return [TextContent(type="text", text=value)]
    
    elif name == "save_memory":
        key = arguments.get("key")
        value = arguments.get("value")
        
        if not key:
            return [TextContent(type="text", text="Error: key parameter is required")]
        if not value:
            return [TextContent(type="text", text="Error: value parameter is required")]
        
        memory_store[key] = value
        logger.info(f"Saved memory for key: {key}")
        
        return [TextContent(type="text", text=f"Memory saved successfully for key: {key}")]
    
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Main entry point for the server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="memory-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())