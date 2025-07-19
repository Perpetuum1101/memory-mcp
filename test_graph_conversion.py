#!/usr/bin/env python3
"""Test script for graph conversion functionality."""

import asyncio
import os
from memory_mcp.server import convert_memory_to_graph, save_memory_as_graph

async def test_graph_conversion():
    """Test the graph conversion functionality."""
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key: export OPENAI_API_KEY='your-key-here'")
        return
    
    # Test memory string with entities and relationships
    test_memory = """
    John works at OpenAI as a software engineer. He is married to Sarah, who is a doctor at Stanford Hospital.
    John and Sarah live in San Francisco. OpenAI is located in San Francisco and was founded by Sam Altman.
    John graduated from MIT with a degree in Computer Science.
    """
    
    print("🧪 Testing graph conversion...")
    print(f"Input memory: {test_memory.strip()}")
    print("\n" + "="*50 + "\n")
    
    try:
        # Test convert_memory_to_graph
        result = await convert_memory_to_graph(test_memory)
        print("✅ Graph conversion result:")
        print(result)
        
        print("\n" + "-"*30 + "\n")
        
        # Test save_memory_as_graph
        result2 = await save_memory_as_graph("test_key", test_memory)
        print("✅ Save memory as graph result:")
        print(result2)
        
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    asyncio.run(test_graph_conversion())