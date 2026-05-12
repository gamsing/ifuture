from __future__ import annotations

import hashlib
import pickle
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Optional


@dataclass(frozen=True)
class CachePolicy:
    enabled: bool = True
    ttl_seconds: Optional[int] = None


class DiskCache:
    def __init__(self, root: Path, policy: CachePolicy | None = None) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.policy = policy or CachePolicy()

    def _path_for_key(self, key: str) -> Path:
        digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
        return self.root / f"{digest}.pkl"

    def get(self, key: str) -> Any:
        if not self.policy.enabled:
            raise KeyError(key)
        p = self._path_for_key(key)
        if not p.exists():
            raise KeyError(key)
        with p.open("rb") as f:
            payload = pickle.load(f)
        if not isinstance(payload, dict) or "ts" not in payload or "value" not in payload:
            raise KeyError(key)
        if self.policy.ttl_seconds is not None:
            if (time.time() - float(payload["ts"])) > self.policy.ttl_seconds:
                raise KeyError(key)
        return payload["value"]

    def set(self, key: str, value: Any) -> None:
        if not self.policy.enabled:
            return
        p = self._path_for_key(key)
        with p.open("wb") as f:
            pickle.dump({"ts": time.time(), "value": value}, f, protocol=pickle.HIGHEST_PROTOCOL)

    def get_or_set(self, key: str, fn: Callable[[], Any]) -> Any:
        try:
            return self.get(key)
        except KeyError:
            value = fn()
            self.set(key, value)
            return value
