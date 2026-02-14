from app_mcp.db.queries import fetch_grouped_errors
from app_mcp.shared.window import resolve_window
from app_mcp.shared.formatters import build_errors_table
from app_mcp.shared.stack import extract_stack_fingerprint


def list_errors_handler(
    window=None,
    session=None,
    session_id=None,
):
    start, end = resolve_window(window)

    rows = fetch_grouped_errors(start, end)

    # attach session-scoped id + fingerprint
    for idx, r in enumerate(rows, start=1):
        r["error_id"] = idx
        r["stack_fingerprint"] = extract_stack_fingerprint(
            r.get("StackTrace", "")
        )

    # store full result set in session
    session["last_errors"] = rows
    session["last_window"] = window
    session["last_error_id"] = rows[0]["error_id"] if rows else None

    table = build_errors_table(rows)

    return {
        "status": "success",
        "data": {
            "total": len(rows),
            "output": table
        }
    }
