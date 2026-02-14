from typing import Dict, Callable
from pydantic import BaseModel
from app_mcp.session.store import get_session


class MCPServer:

    def __init__(self):
        self._tools: Dict[str, dict] = {}

    def register_tool(self, name: str, handler: Callable, schema: type[BaseModel]):
        self._tools[name] = {
            "handler": handler,
            "schema": schema,
        }

    def execute(self, tool: str, args: dict, session_id: str):
        if tool not in self._tools:
            raise ValueError(f"Unknown tool: {tool}")

        tool_def = self._tools[tool]
        validated_args = tool_def["schema"](**args)

        session = get_session(session_id)

        return tool_def["handler"](
            session=session,
            session_id=session_id,
            **validated_args.dict()
        )
