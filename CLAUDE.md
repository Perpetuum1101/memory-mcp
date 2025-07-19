# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Memory Management MCP (Model Context Protocol) server that provides tools for storing and retrieving key-value memory. The server uses FastMCP for simplified MCP server implementation and provides two main tools: `get_memory` and `save_memory`.

## Architecture

The server uses FastMCP for simplified implementation:

- **Server**: `src/memory_mcp/server.py` contains the FastMCP server implementation
- **Storage**: Uses in-memory dictionary storage (`memory_store`) for simplicity
- **Tools**: Provides `get_memory` and `save_memory` tools via `@mcp.tool()` decorators
- **Entry Point**: Server can be run via `memory-mcp` command
- **Framework**: Uses FastMCP from `mcp.server.fastmcp` for simplified server creation
- **Dependencies**: Requires `mcp[cli]` library for FastMCP implementation

## Development Commands

### Installation

```bash
# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

### Running the Server

```bash
# Run as installed command
memory-mcp

# Note: FastMCP servers are typically run via the CLI command above
```

### Testing

```bash
# Run the simple test script
python test_server.py

# Run pytest (when test suite exists)
pytest

# Test the logic without MCP dependencies
python simple_test.py

# Note: Install with 'pip install "mcp[cli]"' for full MCP functionality
```

### Code Quality

```bash
# Format code
black src/

# Lint code
flake8 src/

# Type checking
mypy src/
```

## Specification Management

Transform user commands into structured functional specifications and maintain them in `specs.md`. Each specification must follow this structure:

```
**[SPEC-NNN]** - [Descriptive Title]
- **Functional Requirement**: [What functionality to implement]
- **Implementation Details**:
- Technology/Framework: [Specific technologies to use]
- Components: [What components/modules to create or modify]
- Data Flow: [How data moves through the system]
- **Expected Behavior**:
- Input: [What the system receives]
- Processing: [What the system does]
- Output: [What the system produces]
- **Integration Points**: [How this connects with existing functionality]
- **Constraints**: [Any limitations or specific requirements]
```

Create specs for: Feature requests, functionality changes, new integrations, business logic modifications, API changes, data structure updates

Skip specs for: Code formatting, simple refactoring, documentation updates, bug fixes without functional changes, development setup

## Important Notes

- **Storage Limitation**: Current implementation uses in-memory storage only - data is lost when server restarts
- **MCP Protocol**: Server communicates via stdio and expects MCP-compliant clients
- **FastMCP Design**: Uses simplified FastMCP decorator-based approach instead of manual async handlers
- **Tool Functions**: Tools are regular Python functions decorated with `@mcp.tool()`
