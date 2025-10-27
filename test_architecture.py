#!/usr/bin/env python3
"""
Test script to verify the SP-API CrewAI Chatbot architecture
"""

import requests
import json
import time
import sys
from typing import Dict, Any

def test_endpoint(url: str, method: str = "GET", data: Dict[Any, Any] = None, timeout: int = 10) -> Dict[str, Any]:
    """Test an endpoint and return results"""
    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=timeout)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, timeout=timeout)
        else:
            return {"success": False, "error": f"Unsupported method: {method}"}
        
        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "data": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
            "url": url
        }
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Connection refused", "url": url}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Timeout", "url": url}
    except Exception as e:
        return {"success": False, "error": str(e), "url": url}

def main():
    print("🧪 Testing SP-API CrewAI Chatbot Architecture")
    print("=" * 60)
    
    # Test endpoints
    endpoints = [
        # MCP Server
        {"name": "MCP Server Health", "url": "http://localhost:7000/health", "method": "GET"},
        
        # SP-API Agent System
        {"name": "SP-API Agent Health", "url": "http://localhost:5001/health", "method": "GET"},
        {"name": "SP-API Agent Models", "url": "http://localhost:5001/v1/models", "method": "GET"},
        {"name": "SP-API Agent Session", "url": "http://localhost:5001/v1/sessions", "method": "POST"},
        
        # Backend
        {"name": "Backend Health", "url": "http://localhost:5000/health", "method": "GET"},
        {"name": "Backend SP-Analytics Health", "url": "http://localhost:5000/api/sp-analytics/health", "method": "GET"},
        {"name": "Backend Session", "url": "http://localhost:5000/v1/sessions", "method": "POST"},
        
        # Frontend (if accessible)
        {"name": "Frontend", "url": "http://localhost:3000", "method": "GET"},
    ]
    
    results = []
    
    for endpoint in endpoints:
        print(f"\n🔍 Testing {endpoint['name']}...")
        result = test_endpoint(
            endpoint['url'], 
            endpoint.get('method', 'GET'),
            endpoint.get('data')
        )
        results.append({**endpoint, **result})
        
        if result['success']:
            print(f"✅ {endpoint['name']}: OK")
        else:
            print(f"❌ {endpoint['name']}: {result.get('error', 'Failed')}")
    
    # Test chat completion
    print(f"\n🔍 Testing Chat Completion...")
    chat_data = {
        "messages": [{"role": "user", "content": "Hello, can you help me with my Amazon orders?"}],
        "model": "sp-api-crewai"
    }
    
    chat_result = test_endpoint("http://localhost:5000/v1/chat/completions", "POST", chat_data, timeout=30)
    results.append({
        "name": "Chat Completion",
        "url": "http://localhost:5000/v1/chat/completions",
        "method": "POST",
        **chat_result
    })
    
    if chat_result['success']:
        print("✅ Chat Completion: OK")
    else:
        print(f"❌ Chat Completion: {chat_result.get('error', 'Failed')}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"✅ Successful: {len(successful)}/{len(results)}")
    print(f"❌ Failed: {len(failed)}/{len(results)}")
    
    if failed:
        print("\n❌ FAILED TESTS:")
        for result in failed:
            print(f"  - {result['name']}: {result.get('error', 'Unknown error')}")
    
    print("\n🏗️ ARCHITECTURE STATUS:")
    
    # Check each component
    mcp_ok = any(r['name'] == 'MCP Server Health' and r['success'] for r in results)
    agent_ok = any(r['name'] == 'SP-API Agent Health' and r['success'] for r in results)
    backend_ok = any(r['name'] == 'Backend Health' and r['success'] for r in results)
    frontend_ok = any(r['name'] == 'Frontend' and r['success'] for r in results)
    
    print(f"  🔧 MCP Server (port 7000): {'✅ Running' if mcp_ok else '❌ Not running'}")
    print(f"  🤖 SP-API Agent System (port 5001): {'✅ Running' if agent_ok else '❌ Not running'}")
    print(f"  🌐 Backend (port 5000): {'✅ Running' if backend_ok else '❌ Not running'}")
    print(f"  💻 Frontend (port 3000): {'✅ Running' if frontend_ok else '❌ Not running'}")
    
    if mcp_ok and agent_ok and backend_ok:
        print("\n🎉 Core architecture is working!")
        print("   Frontend → Backend → SP-API Agent System → MCP Server")
    else:
        print("\n⚠️  Some components are not running.")
        print("   Make sure to start all services:")
        print("   - MCP Server: cd sp-api-mcp-server && npm start")
        print("   - SP-API Agent: cd sp-api-agent-system && python sp_api_agent_system.py")
        print("   - Backend: cd backend && python web_interface.py")
        print("   - Frontend: cd frontend && npm start")

if __name__ == "__main__":
    main()
