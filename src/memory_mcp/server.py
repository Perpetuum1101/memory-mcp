"""Memory MCP server implementation using FastMCP."""

import logging
from typing import Dict, List
import asyncio
import os

from mcp.server.fastmcp import FastMCP
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document

# In-memory storage for simplicity
memory_store: Dict[str, str] = {}

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastMCP server instance
mcp = FastMCP("memory-mcp")

# Initialize OpenAI LLM for graph transformation
def get_graph_transformer():
    """Get configured graph transformer with OpenAI LLM"""
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0,
        api_key=openai_api_key
    )
    
    return LLMGraphTransformer(llm=llm)


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


@mcp.tool()
async def convert_memory_to_graph(memory_string: str) -> str:
    """Convert a memory string into graph format using LangChain experimental graph transformer"""
    try:
        # Get the graph transformer
        graph_transformer = get_graph_transformer()
        
        # Create a document from the memory string
        documents = [Document(page_content=memory_string)]
        
        # Convert to graph documents
        graph_documents = await graph_transformer.aconvert_to_graph_documents(documents)
        
        # Format the result
        result = []
        for graph_doc in graph_documents:
            doc_info = {
                "nodes": [],
                "relationships": []
            }
            
            # Extract nodes
            for node in graph_doc.nodes:
                doc_info["nodes"].append({
                    "id": node.id,
                    "type": node.type,
                    "properties": node.properties
                })
            
            # Extract relationships
            for rel in graph_doc.relationships:
                doc_info["relationships"].append({
                    "source": rel.source.id,
                    "target": rel.target.id,
                    "type": rel.type,
                    "properties": rel.properties
                })
            
            result.append(doc_info)
        
        return f"Graph conversion successful. Generated {len(result)} graph documents with {sum(len(doc['nodes']) for doc in result)} nodes and {sum(len(doc['relationships']) for doc in result)} relationships."
        
    except Exception as e:
        logger.error(f"Error converting memory to graph: {str(e)}")
        return f"Error converting memory to graph: {str(e)}"


@mcp.tool()
async def save_memory_as_graph(key: str, memory_string: str) -> str:
    """Save memory as both text and converted graph format"""
    try:
        # Save the original memory string
        memory_store[key] = memory_string
        
        # Convert to graph format
        graph_transformer = get_graph_transformer()
        documents = [Document(page_content=memory_string)]
        graph_documents = await graph_transformer.aconvert_to_graph_documents(documents)
        
        # Store graph representation
        graph_key = f"{key}_graph"
        graph_data = []
        
        for graph_doc in graph_documents:
            doc_info = {
                "nodes": [{"id": node.id, "type": node.type, "properties": node.properties} for node in graph_doc.nodes],
                "relationships": [{"source": rel.source.id, "target": rel.target.id, "type": rel.type, "properties": rel.properties} for rel in graph_doc.relationships]
            }
            graph_data.append(doc_info)
        
        memory_store[graph_key] = str(graph_data)
        
        logger.info(f"Saved memory and graph for key: {key}")
        return f"Memory and graph saved successfully for key: {key}. Graph stored as {graph_key}"
        
    except Exception as e:
        logger.error(f"Error saving memory as graph: {str(e)}")
        return f"Error saving memory as graph: {str(e)}"