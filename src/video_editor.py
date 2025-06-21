"""Video editing utilities for creating clips."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

import ffmpeg


@dataclass
class ClipSegment:
    start: int
    end: int


class VideoEditor:
    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)

    def create_clip(self, video_path: Path, segment: ClipSegment, output: Path) -> Path:
        """Create a clip from a video using ffmpeg."""
        self.logger.info("Creating clip %s", output)
        (
            ffmpeg
            .input(str(video_path), ss=segment.start, to=segment.end)
            .output(str(output))
            .overwrite_output()
            .run(quiet=True)
        )
        return output
