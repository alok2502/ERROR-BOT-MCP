from pydantic import BaseModel
from app_mcp.mcp.server import MCPServer

from app_mcp.handlers.list_errors import list_errors_handler
from app_mcp.handlers.error_details import get_error_details_handler
from app_mcp.handlers.impacted_users import impacted_users_handler
from app_mcp.handlers.error_trend import error_trend_handler
from app_mcp.handlers.top_impacting_errors import top_impacting_errors_handler


def build_mcp_server():
    server = MCPServer()

    class ListErrors(BaseModel):
        session_id: str

    class ErrorDetails(BaseModel):
        session_id: str
        error_id: int

    class ImpactedUsers(BaseModel):
        session_id: str
        error_id: int

    class ErrorTrend(BaseModel):
        session_id: str
        error_id: int

    class TopErrors(BaseModel):
        session_id: str

    server.register_tool("list_errors", list_errors_handler, ListErrors)
    server.register_tool("get_error_details", get_error_details_handler, ErrorDetails)
    server.register_tool("impacted_users", impacted_users_handler, ImpactedUsers)
    server.register_tool("error_trend", error_trend_handler, ErrorTrend)
    server.register_tool("top_impacting_errors", top_impacting_errors_handler, TopErrors)

    return server
