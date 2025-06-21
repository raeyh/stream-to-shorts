"""Manage recorded videos and metadata."""
from __future__ import annotations

import logging
from pathlib import Path
from sqlite3 import Connection, connect


class ContentManager:
    def __init__(self, db_path: Path) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.db_path = db_path
        self.conn: Connection = connect(self.db_path)
        self._init_db()

    def _init_db(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS streams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                streamer TEXT,
                title TEXT,
                filepath TEXT
            )
            """
        )
        self.conn.commit()

    def add_stream(self, streamer: str, title: str, filepath: Path) -> int:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO streams (streamer, title, filepath) VALUES (?, ?, ?)",
            (streamer, title, str(filepath)),
        )
        self.conn.commit()
        return cur.lastrowid
