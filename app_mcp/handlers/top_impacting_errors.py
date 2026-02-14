from collections import defaultdict
from app_mcp.db.queries import fetch_impacted_users
from app_mcp.shared.window import resolve_window
from app_mcp.shared.formatters import build_top_errors_table


def top_impacting_errors_handler(
    window=None,
    limit: int = 5,
    session=None,
    session_id=None,
):
    if not session or "last_errors" not in session:
        return {"status": "error", "message": "Run list_errors first"}

    start, end = resolve_window(window)

    impact = defaultdict(int)

    for error in session["last_errors"]:
        fingerprints = error.get("stack_fingerprint", [])
        if not fingerprints:
            continue

        stack_like = "%" + "%".join(fingerprints[:3]) + "%"

        users = fetch_impacted_users(start, end, stack_like)

        impact[error["error_id"]] = len(users)

    ranked = sorted(
        impact.items(),
        key=lambda x: x[1],
        reverse=True
    )[:limit]

    table = build_top_errors_table(ranked, session["last_errors"])

    return {
        "status": "success",
        "data": {
            "output": table
        }
    }
