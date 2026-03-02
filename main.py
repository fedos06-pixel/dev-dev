import os
import json
from typing import Any, Dict, List
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="MCP Demo Server")

# Конфигурация
DEMO_DIR = os.path.join(os.path.dirname(__file__), "demo_project")

class JsonRpcRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: Dict[str, Any] = {}
    id: Any = None

@app.get("/health")
async def health_check():
    """Endpoint здоровья сервиса для проверки готовности контейнера."""
    return {"status": "healthy", "service": "mcp-demo-server"}

@app.post("/mcp")
async def mcp_endpoint(request: JsonRpcRequest):
    """
    MCP Streamable HTTP endpoint (упрощенная реализация JSON-RPC).
    Обрабатывает вызовы инструментов.
    """
    method = request.method
    params = request.params
    
    response_result = {}
    
    if method == "initialize":
        response_result = {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "demo-mcp-server", "version": "1.0.0"}
        }
    elif method == "tools/list":
        # Возвращаем список доступных инструментов
        response_result = {
            "tools": [
                {
                    "name": "read_demo_file",
                    "description": "Читает содержимое файла из папки demo_project",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "filename": {"type": "string", "description": "Имя файла"}
                        },
                        "required": ["filename"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "read_demo_file":
            filename = arguments.get("filename")
            filepath = os.path.join(DEMO_DIR, filename)
            
            if not os.path.exists(filepath):
                return JSONResponse(content={
                    "jsonrpc": "2.0",
                    "id": request.id,
                    "error": {"code": -32000, "message": f"File {filename} not found"}
                })
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            response_result = {
                "content": [{"type": "text", "text": content}]
            }
        else:
            return JSONResponse(content={
                "jsonrpc": "2.0",
                "id": request.id,
                "error": {"code": -32601, "message": "Tool not found"}
            })
    else:
        return JSONResponse(content={
            "jsonrpc": "2.0",
            "id": request.id,
            "error": {"code": -32601, "message": "Method not found"}
        })

    return {
        "jsonrpc": "2.0",
        "id": request.id,
        "result": response_result
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
