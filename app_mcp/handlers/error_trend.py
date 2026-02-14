from app_mcp.db.trends import fetch_error_trend
from app_mcp.shared.window import resolve_window


def error_trend_handler(
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
        return {"status": "success", "data": {"trend": []}}

    stack_like = "%" + "%".join(fingerprints[:3]) + "%"

    trend = fetch_error_trend(start, end, stack_like)

    return {
        "status": "success",
        "data": {
            "trend": trend
        }
    }
