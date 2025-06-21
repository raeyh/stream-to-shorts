"""Entry point for running the pipeline."""
from __future__ import annotations

import logging
from pathlib import Path

from .stream_monitor import TwitchStreamMonitor, YouTubeStreamMonitor
from .stream_recorder import StreamRecorder
from .content_manager import ContentManager
from .scheduler import Scheduler
from .config_loader import load_config

logging.basicConfig(level=logging.INFO)


def main(config_path: str = "config/default.yml") -> None:
    """Run the stream monitoring pipeline using the given config file."""

    cfg = load_config(Path(config_path))

    recorder = StreamRecorder()
    manager = ContentManager(Path(cfg.storage.get("database", "data.db")))
    sched = Scheduler(recorder, manager, Path(cfg.storage.get("recordings", "recordings")))

    monitors = {}
    creds = cfg.credentials
    twitch_creds = creds.get("twitch")
    if twitch_creds:
        monitors["twitch"] = TwitchStreamMonitor(
            client_id=twitch_creds["client_id"],
            oauth_token=twitch_creds["oauth_token"],
        )
    youtube_creds = creds.get("youtube")
    if youtube_creds:
        monitors["youtube"] = YouTubeStreamMonitor(api_key=youtube_creds["api_key"])

    for stream in cfg.streams:
        platform = stream.get("platform")
        username = stream.get("username")
        quality = stream.get("quality", "best")
        monitor = monitors.get(platform)
        if monitor is None:
            logging.warning("No credentials configured for platform %s", platform)
            continue
        sched.add_stream(monitor, username, quality)

    sched.start(cfg.scheduler.get("interval", 60))


if __name__ == "__main__":
    main()

