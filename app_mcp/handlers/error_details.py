from app_mcp.shared.formatters import build_error_details_md


def get_error_details_handler(
    error_id: int | None = None,
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

    return {
        "status": "success",
        "data": {
            "output": build_error_details_md(error)
        }
    }
