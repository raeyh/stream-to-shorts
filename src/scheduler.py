"""Pipeline orchestration using APScheduler."""
from __future__ import annotations

import logging
from typing import Dict, List

from apscheduler.schedulers.background import BackgroundScheduler

from .stream_monitor import BaseStreamMonitor, StreamMonitor
from .stream_recorder import RecordingConfig, StreamRecorder
from .content_manager import ContentManager


class Scheduler:
    def __init__(self, recorder: StreamRecorder, manager: ContentManager) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.recorder = recorder
        self.manager = manager
        self.monitors: Dict[BaseStreamMonitor, List[str]] = {}
        self.sched = BackgroundScheduler()

    def add_monitor(self, monitor: BaseStreamMonitor, users: List[str]) -> None:
        """Register a monitor with the scheduler."""
        self.monitors[monitor] = users

    def start(self, interval: int = 60) -> None:
        self.logger.info("Starting scheduler")
        self.sched.add_job(self.check_streams, 'interval', seconds=interval)
        self.sched.start()

    def check_streams(self) -> None:
        for monitor, users in self.monitors.items():
            streams = monitor.get_live_streams(users)
            for stream in streams:
                path = self.recorder.record(RecordingConfig(url=stream.url))
                self.manager.add_stream(stream.streamer, stream.title, path)
