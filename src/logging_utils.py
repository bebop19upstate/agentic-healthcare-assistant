import csv
import time
import os
from contextlib import contextmanager

LOG_PATH = "data/tool_call_log.csv"


def log_tool_call(tool_name: str, success: bool, latency_ms: float) -> None:
    file_exists = os.path.exists(LOG_PATH)
    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["tool_name", "success", "latency_ms"])
        writer.writerow([tool_name, success, round(latency_ms, 1)])


@contextmanager
def timed_tool_call(tool_name: str):
    start = time.time()
    success = True
    try:
        yield
    except Exception:
        success = False
        raise
    finally:
        latency_ms = (time.time() - start) * 1000
        log_tool_call(tool_name, success, latency_ms)
