import time
from typing import Any, Optional
from datetime import datetime


class SimpleCache:
    """Simple in-memory cache with TTL support"""

    def __init__(self):
        self._cache: dict[str, dict[str, Any]] = {}

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if key not in self._cache:
            return None

        cache_entry = self._cache[key]
        if time.time() > cache_entry['expires_at']:
            # Cache expired, remove it
            del self._cache[key]
            return None

        return cache_entry['value']

    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """Set value in cache with TTL (seconds)"""
        self._cache[key] = {
            'value': value,
            'expires_at': time.time() + ttl,
            'created_at': datetime.now()
        }

    def delete(self, key: str) -> None:
        """Delete key from cache"""
        if key in self._cache:
            del self._cache[key]

    def clear(self) -> None:
        """Clear all cache"""
        self._cache.clear()

    def get_stats(self) -> dict[str, Any]:
        """Get cache statistics"""
        active_entries = 0
        expired_entries = 0
        current_time = time.time()

        for _, entry in self._cache.items():
            if current_time > entry['expires_at']:
                expired_entries += 1
            else:
                active_entries += 1

        return {
            'total_entries': len(self._cache),
            'active_entries': active_entries,
            'expired_entries': expired_entries
        }

    def cleanup_expired(self) -> int:
        """Remove expired entries and return count"""
        current_time = time.time()
        expired_keys = [
            key for key, entry in self._cache.items()
            if current_time > entry['expires_at']
        ]

        for key in expired_keys:
            del self._cache[key]

        return len(expired_keys)


# Global cache instance
cache = SimpleCache()
