"""Pipeline orchestration using APScheduler."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from apscheduler.schedulers.background import BackgroundScheduler

from .stream_monitor import BaseStreamMonitor, StreamMonitor
from .stream_recorder import RecordingConfig, StreamRecorder
from .content_manager import ContentManager


@dataclass
class StreamSpec:
    """Specification for a stream to monitor."""

    username: str
    quality: str = "best"


class Scheduler:
    def __init__(self, recorder: StreamRecorder, manager: ContentManager, output_dir: Path) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.recorder = recorder
        self.manager = manager
        self.output_dir = output_dir
        self.monitors: Dict[BaseStreamMonitor, List[StreamSpec]] = {}
        self.sched = BackgroundScheduler()

    def add_stream(self, monitor: BaseStreamMonitor, username: str, quality: str = "best") -> None:
        """Register a stream with the scheduler."""
        specs = self.monitors.setdefault(monitor, [])
        specs.append(StreamSpec(username=username, quality=quality))

    def start(self, interval: int = 60) -> None:
        self.logger.info("Starting scheduler")
        self.sched.add_job(self.check_streams, "interval", seconds=interval)
        self.sched.start()

    def check_streams(self) -> None:
        for monitor, specs in self.monitors.items():
            usernames = [s.username for s in specs]
            streams = monitor.get_live_streams(usernames)
            spec_map = {s.username: s for s in specs}
            for stream in streams:
                spec = spec_map.get(stream.streamer)
                cfg = RecordingConfig(
                    url=stream.url,
                    quality=spec.quality if spec else "best",
                    output=self.output_dir,
                )
                path = self.recorder.record(cfg)
                self.manager.add_stream(stream.streamer, stream.title, path)

