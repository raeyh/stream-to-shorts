"""Stream recording utilities using streamlink."""
from __future__ import annotations

import logging
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class RecordingConfig:
    url: str
    quality: str = "best"
    output: Path = Path("recordings")


class StreamRecorder:
    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)

    def record(self, config: RecordingConfig) -> Path:
        """Record a stream using streamlink."""
        output_dir = config.output
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{Path(config.url).name}.mp4"
        cmd = [
            "streamlink",
            config.url,
            config.quality,
            "-o",
            str(output_file),
        ]
        self.logger.info("Recording %s", config.url)
        subprocess.run(cmd, check=True)
        return output_file
