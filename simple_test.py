"""Simple test without MCP dependency to check logic."""

# Simulate the memory store and functions without MCP
memory_store = {}

def get_memory(key: str) -> str:
    """Retrieve stored memory by key"""
    value = memory_store.get(key)
    if value is None:
        return f"No memory found for key: {key}"
    return value

def save_memory(key: str, value: str) -> str:
    """Save memory with a key"""
    memory_store[key] = value
    return f"Memory saved successfully for key: {key}"

def test_memory_functions():
    """Test the memory functions."""
    print("Testing memory logic...")
    
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