from concurrent.futures import ThreadPoolExecutor, TimeoutError as FUTimeout
from functools import wraps
from .errors import ContractViolation, StopSignal

def guarded_step(name: str, timeout: int | None = None):
    """Wrap a step with timeout and basic error mapping. Telemetry is intentionally minimal here."""
    def deco(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            to = kwargs.pop("timeout", timeout)
            if to:
                with ThreadPoolExecutor(max_workers=1) as ex:
                    fut = ex.submit(fn, *args, **kwargs)
                    try:
                        return fut.result(timeout=to)
                    except FUTimeout:
                        raise StopSignal(f"{name} timeout {to}s")
            return fn(*args, **kwargs)
        return wrapper
    return deco