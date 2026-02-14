from app_mcp.db.queries import fetch_impacted_users
from app_mcp.shared.window import resolve_window
from app_mcp.shared.formatters import build_impacted_users_table


def impacted_users_handler(
    error_id: int | None = None,
    window=None,
    session=None,
    session_id=None,
):
    if not session or "last_errors" not in session:
        return {"status": "error", "message": "Run list_errors first"}

    if error_id is None:
        error_id = session.get("last_error_id")

    error = next(
        (r for r in session["last_errors"] if r["error_id"] == error_id),
        None
    )

    if not error:
        return {"status": "error", "message": "Invalid error_id"}

    session["last_error_id"] = error_id

    start, end = resolve_window(window)

    fingerprints = error.get("stack_fingerprint", [])
    if not fingerprints:
        return {"status": "success", "data": {"output": "No fingerprint available"}}

    stack_like = "%" + "%".join(fingerprints[:3]) + "%"

    users = fetch_impacted_users(start, end, stack_like)

    table = build_impacted_users_table(
        error_id,
        users,
        start,
        end
    )

    return {
        "status": "success",
        "data": {
            "total": len(users),
            "output": table
        }
    }
