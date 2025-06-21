from __future__ import annotations

"""Registry for streaming platform monitors."""

from typing import Dict, Type

from .stream_monitor import (
    BaseStreamMonitor,
    TwitchStreamMonitor,
    YouTubeStreamMonitor,
)

PLATFORMS: Dict[str, Type[BaseStreamMonitor]] = {
    "twitch": TwitchStreamMonitor,
    "youtube": YouTubeStreamMonitor,
}


def get_monitor(platform: str, **kwargs) -> BaseStreamMonitor:
    """Return a monitor instance for the given platform."""
    monitor_cls = PLATFORMS.get(platform.lower())
    if monitor_cls is None:
        raise ValueError(f"Unsupported platform: {platform}")
    return monitor_cls(**kwargs)
