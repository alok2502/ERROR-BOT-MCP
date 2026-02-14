from datetime import datetime, timedelta
from typing import Optional


class WindowSpec:
    def __init__(self, last_days: Optional[int] = None,
                 start: Optional[str] = None,
                 end: Optional[str] = None):
        self.last_days = last_days
        self.start = start
        self.end = end


def resolve_window(window: Optional[WindowSpec]):
    now = datetime.utcnow()

    if not window:
        return now - timedelta(days=1), now

    if window.last_days:
        return now - timedelta(days=window.last_days), now

    if window.start and window.end:
        return datetime.fromisoformat(window.start), datetime.fromisoformat(window.end)

    return now - timedelta(days=1), now
