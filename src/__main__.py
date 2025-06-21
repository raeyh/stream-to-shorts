"""Entry point for running the pipeline."""
from __future__ import annotations

import logging
from pathlib import Path

from .stream_monitor import TwitchStreamMonitor, YouTubeStreamMonitor
from .stream_recorder import StreamRecorder
from .content_manager import ContentManager
from .scheduler import Scheduler

logging.basicConfig(level=logging.INFO)


def main() -> None:
    twitch_monitor = TwitchStreamMonitor(
        client_id="YOUR_CLIENT_ID", oauth_token="YOUR_TOKEN"
    )
    # Example: add a YouTube monitor
    # youtube_monitor = YouTubeStreamMonitor(api_key="YOUR_API_KEY")

    recorder = StreamRecorder()
    manager = ContentManager(Path("data.db"))
    sched = Scheduler(recorder, manager)
    sched.add_monitor(twitch_monitor, ["example_streamer"])  # replace with Twitch streamers
    # sched.add_monitor(youtube_monitor, ["CHANNEL_ID"])  # add YouTube channels
    sched.start()


if __name__ == "__main__":
    main()
