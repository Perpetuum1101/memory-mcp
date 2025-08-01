"""Simple test script for the FastMCP server."""

from src.memory_mcp.server import get_memory, save_memory


def test_memory_functions():
    """Test the memory functions."""
    print("Testing FastMCP server tools...")
    
    # Test save_memory
    save_result = save_memory("test_key", "test_value")
    print(f"Save result: {save_result}")
    
    # Test get_memory
    get_result = get_memory("test_key")
    print(f"Get result: {get_result}")
    
    # Test get_memory for non-existent key
    get_missing = get_memory("missing_key")
    print(f"Missing key result: {get_missing}")
    
    print("All tests completed!")


if __name__ == "__main__":
    test_memory_functions()