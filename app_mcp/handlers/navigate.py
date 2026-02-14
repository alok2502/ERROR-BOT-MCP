from app_mcp.handlers.list_errors import list_errors_handler


def navigate_handler(
    direction: str,
    session=None,
    session_id=None,
):
    if not session or "last_errors" not in session:
        return {"status": "error", "message": "Run list_errors first"}

    # simple re-run using stored window
    return list_errors_handler(
        window=session.get("last_window"),
        session=session,
        session_id=session_id
    )
