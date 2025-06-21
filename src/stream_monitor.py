"""Twitch stream monitoring utilities."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import List, Dict, Optional

import requests


@dataclass
class StreamInfo:
    """Metadata about a Twitch stream."""

    streamer: str
    title: str
    game: Optional[str]
    viewer_count: int
    url: str


class StreamMonitor:
    """Monitor Twitch for live streams."""

    def __init__(self, client_id: str, oauth_token: str) -> None:
        self.client_id = client_id
        self.oauth_token = oauth_token
        self.base_url = "https://api.twitch.tv/helix/streams"
        self.logger = logging.getLogger(self.__class__.__name__)

    def _headers(self) -> Dict[str, str]:
        return {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.oauth_token}",
        }

    def get_live_streams(self, user_logins: List[str]) -> List[StreamInfo]:
        """Return metadata for live streams from a list of usernames."""
        params = [("user_login", login) for login in user_logins]
        self.logger.debug("Fetching live streams for %s", user_logins)
        resp = requests.get(self.base_url, headers=self._headers(), params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json().get("data", [])
        streams = []
        for item in data:
            streams.append(
                StreamInfo(
                    streamer=item.get("user_login"),
                    title=item.get("title"),
                    game=item.get("game_name"),
                    viewer_count=item.get("viewer_count", 0),
                    url=f"https://twitch.tv/{item.get('user_login')}",
                )
            )
        return streams
