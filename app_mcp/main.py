from app_mcp.mcp.registry import build_mcp_server

mcp_server = build_mcp_server()


def run_mcp(payload: dict):
    return mcp_server.execute(
        tool=payload["tool"],
        args=payload.get("args", {}),
        session_id=payload["session_id"],
    )
