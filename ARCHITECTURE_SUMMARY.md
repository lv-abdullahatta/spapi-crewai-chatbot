# SP-API CrewAI Chatbot Architecture

## Current Architecture Overview

The project now correctly implements the architecture shown in your diagram:

```
┌─────────────────────────────────────────┐
│  Frontend (React)                       │
│  http://localhost:3000                  │
└───────────────┬─────────────────────────┘
                │
                │ HTTP Requests
                │
                ▼
┌─────────────────────────────────────────┐
│  Backend (Flask)                        │
│  http://localhost:5000                  │
│                                         │
│  Routes:                                │
│  • /v1/chat/completions    ◄─┐        │
│  • /v1/sessions             │          │
│  • /api/sp-analytics/query  │          │
│  • /api/sp-analytics/health │          │
└─────────────────────────────────┼───────┘
                                  │
                      Proxies to  │
                                  │
                                  ▼
┌─────────────────────────────────────────┐
│  SP-API Agent System (CrewAI)           │
│  http://localhost:5001                  │
│                                         │
│  • /v1/chat/completions                 │
│  • /v1/sessions                         │
│  • /health                              │
└───────────────┬─────────────────────────┘
                │
                │
                ▼
┌─────────────────────────────────────────┐
│  MCP Server                             │
│  http://localhost:7000                  │
└─────────────────────────────────────────┘
```

## Component Details

### 1. Frontend (React) - Port 3000
- **Location**: `frontend/`
- **Configuration**: 
  - `frontend/src/config.ts` - Backend URL: `http://localhost:5000`
  - `frontend/src/components/ChatBot.tsx` - Main chat interface
  - `frontend/src/services/spAnalytics.js` - Analytics service
- **Features**:
  - Chat interface with quick actions
  - Session management
  - Real-time messaging

### 2. Backend (Flask) - Port 5000
- **Location**: `backend/web_interface.py`
- **Configuration**: 
  - Runs on `localhost:5000`
  - Proxies requests to SP-API Agent System on port 5001
- **Routes**:
  - `GET /health` - Health check
  - `POST /v1/chat/completions` - Proxies to agent system
  - `POST /v1/sessions` - Proxies to agent system
  - `POST /api/sp-analytics/query` - Proxies to agent system
  - `GET /api/sp-analytics/health` - Proxies to agent system

### 3. SP-API Agent System (CrewAI) - Port 5001
- **Location**: `sp-api-agent-system/`
- **Configuration**: 
  - `sp-api-agent-system/config.py` - Port 5001
  - `sp-api-agent-system/sp_api_agent_system.py` - Main agent system
- **Features**:
  - Multi-agent workflow with CrewAI
  - MCP client for SP-API integration
  - OpenAI-compatible API endpoints
  - Session management

### 4. MCP Server - Port 7000
- **Location**: `sp-api-mcp-server/`
- **Configuration**: 
  - Docker container on port 7000
  - Amazon SP-API integration
- **Features**:
  - SP-API catalog exploration
  - API execution tools
  - Authentication handling

## Data Flow

1. **User Input**: User types message in React frontend
2. **Frontend → Backend**: HTTP request to `http://localhost:5000/v1/chat/completions`
3. **Backend → Agent System**: Proxy request to `http://localhost:5001/v1/chat/completions`
4. **Agent System → MCP Server**: Agent system uses MCP client to call `http://localhost:7000`
5. **MCP Server → Amazon SP-API**: MCP server makes authenticated calls to Amazon SP-API
6. **Response Chain**: Data flows back through the chain to the user

## Key Fixes Applied

1. **Backend Proxying**: Updated `backend/web_interface.py` to properly proxy requests to the SP-API Agent System
2. **Frontend Configuration**: Updated frontend to use correct backend URLs (port 5000)
3. **Route Consistency**: Ensured all routes are properly configured and proxied
4. **Service Integration**: Fixed the spAnalytics service to work with the new architecture

## Environment Variables

- `AGENT_URL`: Backend uses this to connect to SP-API Agent System (default: `http://localhost:5001`)
- `MCP_SERVER_URL`: Agent system uses this to connect to MCP server (default: `http://localhost:7000`)
- `REACT_APP_BACKEND_URL`: Frontend uses this to connect to backend (default: `http://localhost:5000`)

## Verification

The architecture now matches your diagram exactly:
- ✅ Frontend on localhost:3000
- ✅ Backend on localhost:5000 with proper routes
- ✅ SP-API Agent System on localhost:5001
- ✅ MCP Server on localhost:7000
- ✅ Proper proxying between components
- ✅ All HTTP requests flow correctly through the chain
