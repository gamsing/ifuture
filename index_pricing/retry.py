from __future__ import annotations

import time
from functools import wraps
from typing import Any, Callable, TypeVar

T = TypeVar("T")


def with_retry(max_retries: int = 3, delay_seconds: float = 1.5) -> Callable[[Callable[..., T]], Callable[..., T]]:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exc: Exception | None = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:  # noqa: BLE001 - intentional boundary for API failures
                    last_exc = e
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(delay_seconds * (2**attempt))
            assert last_exc is not None
            raise last_exc

        return wrapper

    return decorator
