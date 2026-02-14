import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app_mcp.main import run_mcp

app = FastAPI(title="Error Monitor MCP")


@app.post("/mcp")
async def mcp_endpoint(req: Request):

    payload = await req.json()
    method = payload.get("method")
    id_ = payload.get("id")
    params = payload.get("params") or {}

    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments") or {}

        result = run_mcp({
            "tool": name,
            "args": args,
            "session_id": args.get("session_id"),
        })

        return JSONResponse({
            "jsonrpc": "2.0",
            "id": id_,
            "result": {
                "content": [
                    {"type": "text", "text": json.dumps(result)}
                ]
            }
        })

    return JSONResponse({
        "jsonrpc": "2.0",
        "id": id_,
        "error": {"code": -32601, "message": "Method not found"}
    })
