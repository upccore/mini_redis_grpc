import threading
import time
from collections import OrderedDict

LRU_CAPACITY = 10


class KVStore:
    def __init__(self):
        self._data: OrderedDict[str, tuple[str, float | None]] = OrderedDict()
        self._lock = threading.Lock()

    def put(self, key: str, value: str, ttl_seconds: int) -> None:
        expires_at = time.time() + ttl_seconds if ttl_seconds > 0 else None
        with self._lock:
            if key in self._data:
                self._data.move_to_end(key)
            self._data[key] = (value, expires_at)
            if len(self._data) > LRU_CAPACITY:
                self._data.popitem(last=False)

    def get(self, key: str) -> str | None:
        with self._lock:
            if key not in self._data:
                return None
            value, expires_at = self._data[key]
            if expires_at is not None and time.time() > expires_at:
                del self._data[key]
                return None
            self._data.move_to_end(key)
            return value

    def delete(self, key: str) -> None:
        with self._lock:
            self._data.pop(key, None)

    def list_prefix(self, prefix: str) -> list[tuple[str, str]]:
        now = time.time()
        with self._lock:
            return [
                (k, v)
                for k, (v, expires_at) in self._data.items()
                if k.startswith(prefix) and (expires_at is None or now <= expires_at)
            ]
