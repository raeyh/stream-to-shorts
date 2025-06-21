"""Pipeline orchestration using APScheduler."""
from __future__ import annotations

import logging
from typing import List

from apscheduler.schedulers.background import BackgroundScheduler

from .stream_monitor import StreamMonitor
from .stream_recorder import RecordingConfig, StreamRecorder
from .content_manager import ContentManager


class Scheduler:
    def __init__(self, monitor: StreamMonitor, recorder: StreamRecorder, manager: ContentManager) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.monitor = monitor
        self.recorder = recorder
        self.manager = manager
        self.sched = BackgroundScheduler()

    def start(self, users: List[str], interval: int = 60) -> None:
        self.logger.info("Starting scheduler")
        self.sched.add_job(lambda: self.check_streams(users), 'interval', seconds=interval)
        self.sched.start()

    def check_streams(self, users: List[str]) -> None:
        streams = self.monitor.get_live_streams(users)
        for stream in streams:
            path = self.recorder.record(RecordingConfig(url=stream.url))
            self.manager.add_stream(stream.streamer, stream.title, path)
