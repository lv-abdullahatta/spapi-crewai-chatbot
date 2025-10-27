# MCP Server Configuration Update Summary

## Overview
Updated the SP-API Agent System to work with the production MCP server at `https://mcp-server-816670507109.us-east1.run.app/mcp` using the correct authentication and communication protocol.

## Key Findings

### MCP Server Tools Discovered
The MCP server provides **2 tools**:

1. **execute-sp-api**
   - Execute Amazon Selling Partner API requests with authenticated access
   - Parameters:
     - `endpoint` (required): SP-API endpoint name (e.g., 'getOrders')
     - `parameters` (required): API parameters for the endpoint
     - `method`: HTTP method (optional, auto-detected)
     - `region`: AWS region (default: 'us-east-1')
     - `rawMode`: Return raw response
     - `generateCode`: Generate code snippet

2. **explore-sp-api-catalog**
   - Explore SP-API endpoints, get documentation, and discover operations
   - Parameters:
     - `endpoint`: Specific endpoint to get details for
     - `category`: Category to explore
     - `listEndpoints`: List all available endpoints
     - `listCategories`: List all available categories
     - `depth`: Control nested object expansion
     - `ref`: Extract specific nested object

### Authentication Requirements
The MCP server requires:
- **SP-API Access Token** in `X-Amz-Access-Token` header
- **JSON-RPC 2.0 format** for all requests
- **Endpoint**: `/mcp` (not `/api/execute` or `/api/explore`)

## Changes Made

### 1. Configuration (`config.py`)
**Added SP-API Credentials:**
```python
# Amazon SP-API Credentials (required for MCP authentication)
SP_API_CLIENT_ID: str
SP_API_CLIENT_SECRET: str
SP_API_REFRESH_TOKEN: str
```

These credentials are used to obtain access tokens for authenticating with the MCP server.

### 2. SP-API Agent System (`sp_api_agent_system.py`)

#### Added TokenManager Class
```python
class TokenManager:
    """Manages Amazon SP-API access tokens with automatic refresh"""
```
- Automatically refreshes SP-API access tokens
- Caches tokens for 55 minutes (safe margin before 1-hour expiry)
- Integrates with Amazon's OAuth endpoint

#### Updated MCPHTTPClient
**Constructor:**
- Now accepts `token_manager` parameter for authentication

**Health Check Fix:**
- Extracts root URL to check health at `/health` instead of `/mcp/health`
- Accepts both "ok" and "healthy" status values

**API Call Method (`call_endpoint`):**
- ✅ Uses JSON-RPC 2.0 format
- ✅ Includes `X-Amz-Access-Token` header with fresh access token
- ✅ Calls the `execute-sp-api` tool via `tools/call` method
- ✅ Properly extracts content from MCP responses

**Catalog Loading (`_load_catalog`):**
- ✅ Uses JSON-RPC 2.0 format
- ✅ Includes authentication headers
- ✅ Calls the `explore-sp-api-catalog` tool

**Global Initialization:**
```python
# Global token manager and MCP client instance
token_manager = TokenManager(
    Config.SP_API_CLIENT_ID,
    Config.SP_API_CLIENT_SECRET,
    Config.SP_API_REFRESH_TOKEN
)
mcp_client = MCPHTTPClient(token_manager=token_manager)
```

## Request Format Changes

### Before (Old Format)
```python
# POST to /api/execute
{
    "endpoint": "getOrders",
    "parameters": {...},
    "method": "GET",
    "region": "us-east-1"
}
```

### After (JSON-RPC 2.0 Format)
```python
# POST to /mcp
{
    "jsonrpc": "2.0",
    "id": 1234567890,
    "method": "tools/call",
    "params": {
        "name": "execute-sp-api",
        "arguments": {
            "endpoint": "getOrders",
            "parameters": {...}
        }
    }
}

# With headers:
{
    "X-Amz-Access-Token": "Atza|...",
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream"
}
```

## Health Check Endpoints

- **MCP Server Health**: `https://mcp-server-816670507109.us-east1.run.app/health` ✅
- **Cache Stats**: `https://mcp-server-816670507109.us-east1.run.app/cache-stats` ✅
- **MCP Endpoint**: `https://mcp-server-816670507109.us-east1.run.app/mcp` (requires auth)

## Testing

To test the updated system:

```bash
cd sp-api-agent-system
python sp_api_agent_system.py
```

The system will:
1. Get an SP-API access token from Amazon OAuth
2. Connect to the MCP server with authentication
3. Load the catalog of available SP-API endpoints
4. Start the Flask API server on port 5001

## Credentials Source

All credentials are from the working `langgraph_client.py` file:
- SP-API Client ID
- SP-API Client Secret
- SP-API Refresh Token
- OpenAI API Key
- MCP Server URL

## Next Steps

1. ✅ Test the connection to ensure it works
2. ✅ Verify that SP-API calls execute successfully
3. ✅ Monitor token refresh behavior
4. Consider moving credentials to environment variables for better security

## Reference Files

- Working example: `langgraph_client.py` (from Downloads)
- Updated config: `sp-api-agent-system/config.py`
- Updated system: `sp-api-agent-system/sp_api_agent_system.py`

