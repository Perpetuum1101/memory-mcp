"""Memory MCP server implementation using FastMCP."""

import logging
from typing import Dict

from mcp.server.fastmcp import FastMCP

# In-memory storage for simplicity
memory_store: Dict[str, str] = {}

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastMCP server instance
mcp = FastMCP("memory-mcp")


@mcp.tool()
def get_memory(key: str) -> str:
    """Retrieve stored memory by key"""
    value = memory_store.get(key)
    if value is None:
        return f"No memory found for key: {key}"
    return value


@mcp.tool()
def save_memory(key: str, value: str) -> str:
    """Save memory with a key"""
    memory_store[key] = value
    logger.info(f"Saved memory for key: {key}")
    return f"Memory saved successfully for key: {key}"