"""Stream monitoring utilities.

This module now provides a small abstraction layer that makes it possible to
support multiple streaming platforms.  The original Twitch specific monitor is
kept for backwards compatibility and a basic YouTube implementation is
included as an example.  Additional platforms can be added by creating new
classes that implement :class:`BaseStreamMonitor`.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Protocol

import requests


@dataclass
class StreamInfo:
    """Metadata about a Twitch stream."""

    streamer: str
    title: str
    game: Optional[str]
    viewer_count: int
    url: str


class BaseStreamMonitor(Protocol):
    """Interface for a streaming platform monitor."""

    def get_live_streams(self, user_logins: List[str]) -> List[StreamInfo]:
        """Return metadata for live streams from a list of usernames."""


class TwitchStreamMonitor:
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
        params = [("user_login", login) for login in user_logins]
        self.logger.debug("Fetching live streams for %s", user_logins)
        resp = requests.get(
            self.base_url, headers=self._headers(), params=params, timeout=10
        )
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


class YouTubeStreamMonitor:
    """Basic YouTube live stream monitor using the Data API."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3/search"
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_live_streams(self, channel_ids: List[str]) -> List[StreamInfo]:
        streams = []
        for cid in channel_ids:
            params = {
                "part": "snippet",
                "channelId": cid,
                "type": "video",
                "eventType": "live",
                "key": self.api_key,
            }
            self.logger.debug("Fetching live streams for channel %s", cid)
            resp = requests.get(self.base_url, params=params, timeout=10)
            resp.raise_for_status()
            items = resp.json().get("items", [])
            for item in items:
                snippet = item.get("snippet", {})
                streams.append(
                    StreamInfo(
                        streamer=snippet.get("channelTitle", cid),
                        title=snippet.get("title"),
                        game=None,
                        viewer_count=0,
                        url=f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    )
                )
        return streams


# Backwards compatibility: previously the Twitch implementation was named
# ``StreamMonitor``.  Export the Twitch monitor under that name so existing
# imports continue to work.
StreamMonitor = TwitchStreamMonitor
