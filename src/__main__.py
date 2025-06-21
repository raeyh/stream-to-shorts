"""Entry point for running the pipeline."""
from __future__ import annotations

import logging
from pathlib import Path

from .stream_monitor import StreamMonitor
from .stream_recorder import StreamRecorder
from .content_manager import ContentManager
from .scheduler import Scheduler

logging.basicConfig(level=logging.INFO)


def main() -> None:
    monitor = StreamMonitor(client_id="YOUR_CLIENT_ID", oauth_token="YOUR_TOKEN")
    recorder = StreamRecorder()
    manager = ContentManager(Path("data.db"))
    sched = Scheduler(monitor, recorder, manager)
    sched.start(["example_streamer"])  # replace with desired streamers


if __name__ == "__main__":
    main()
