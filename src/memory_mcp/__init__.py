"""Memory MCP server package."""

__version__ = "0.1.0"

from .server import mcp, get_memory, save_memory

__all__ = ["mcp", "get_memory", "save_memory"]