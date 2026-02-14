SESSION_STORE: dict[str, dict] = {}


def get_session(session_id: str) -> dict:
    return SESSION_STORE.setdefault(session_id, {})
