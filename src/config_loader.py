from __future__ import annotations

"""Utilities for loading application configuration."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import yaml


@dataclass
class Config:
    """Container for application configuration."""

    streams: List[Dict[str, Any]]
    storage: Dict[str, Any]
    scheduler: Dict[str, Any]
    credentials: Dict[str, Dict[str, str]]


def load_config(path: Path) -> Config:
    """Load configuration from a YAML file."""
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    return Config(
        streams=data.get("streams", []),
        storage=data.get("storage", {}),
        scheduler=data.get("scheduler", {}),
        credentials=data.get("credentials", {}),
    )
