import os
from datetime import datetime, timedelta, timezone

def window_from_env():
    start = os.getenv("START_TIME")
    end = os.getenv("END_TIME")
    if not start:
        end_dt = datetime.now(timezone.utc)
        start_dt = end_dt - timedelta(days=7)
        return start_dt.isoformat(), end_dt.isoformat()
    return start, end or datetime.now(timezone.utc).isoformat()
