# Vector DB MCP Server

A Model Context Protocol (MCP) server that provides Vector Database integration (Pinecone) for AI agents.

## Features

- Vector storage and retrieval
- Semantic search capabilities
- Namespace support
- Metadata storage
- Health monitoring

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
PINECONE_API_KEY=your_api_key
PINECONE_ENV=your_environment
PINECONE_INDEX=your_index_name
```

3. Run server:
```bash
uvicorn src.mcp_server:app --reload
```

## API Endpoints

- POST /upsert - Store vectors
- POST /search - Search vectors
- GET /health - Check server health

## Example Usage

```python
# Store vectors
POST /upsert
{
    "texts": ["example text 1", "example text 2"],
    "namespace": "my-namespace",
    "metadata": {"key": "value"}
}

# Search vectors
POST /search
{
    "query": "search query",
    "namespace": "my-namespace",
    "top_k": 5
}
```

## MCP Integration

This server follows the MCP specification for tool integration with AI agents.