from __future__ import annotations

import json
import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Iterator

from .config import database_path


class Database:
    def __init__(self) -> None:
        self.path = database_path()
        self._lock = threading.Lock()
        self.initialize()

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def initialize(self) -> None:
        with self._lock:
            with self.connect() as conn:
                conn.executescript(
                    """
                    CREATE TABLE IF NOT EXISTS settings (
                        key TEXT PRIMARY KEY,
                        value TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    );

                    CREATE TABLE IF NOT EXISTS exam_attempts (
                        id TEXT PRIMARY KEY,
                        subject_code TEXT NOT NULL,
                        subject_name TEXT NOT NULL,
                        exam_mode TEXT NOT NULL,
                        title TEXT NOT NULL,
                        started_at TEXT NOT NULL,
                        submitted_at TEXT,
                        total_score REAL NOT NULL,
                        obtained_score REAL NOT NULL,
                        correct_rate REAL NOT NULL,
                        ai_used INTEGER NOT NULL DEFAULT 0,
                        blueprint_json TEXT NOT NULL,
                        exam_json TEXT NOT NULL,
                        answers_json TEXT NOT NULL,
                        result_json TEXT NOT NULL
                    );
                    """
                )

    def get_setting(self, key: str, default: Any = None) -> Any:
        with self.connect() as conn:
            row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
        if not row:
            return default
        return json.loads(row["value"])

    def set_setting(self, key: str, value: Any) -> None:
        payload = json.dumps(value, ensure_ascii=False)
        now = datetime.now().isoformat(timespec="seconds")
        with self._lock:
            with self.connect() as conn:
                conn.execute(
                    """
                    INSERT INTO settings(key, value, updated_at)
                    VALUES(?, ?, ?)
                    ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at
                    """,
                    (key, payload, now),
                )

    def insert_attempt(self, payload: dict[str, Any]) -> None:
        with self._lock:
            with self.connect() as conn:
                conn.execute(
                    """
                    INSERT INTO exam_attempts(
                        id, subject_code, subject_name, exam_mode, title, started_at, submitted_at,
                        total_score, obtained_score, correct_rate, ai_used,
                        blueprint_json, exam_json, answers_json, result_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        payload["id"],
                        payload["subject_code"],
                        payload["subject_name"],
                        payload["exam_mode"],
                        payload["title"],
                        payload["started_at"],
                        payload["submitted_at"],
                        payload["total_score"],
                        payload["obtained_score"],
                        payload["correct_rate"],
                        1 if payload["ai_used"] else 0,
                        json.dumps(payload["blueprint"], ensure_ascii=False),
                        json.dumps(payload["exam"], ensure_ascii=False),
                        json.dumps(payload["answers"], ensure_ascii=False),
                        json.dumps(payload["result"], ensure_ascii=False),
                    ),
                )

    def list_attempts(self, subject_code: str | None = None) -> list[dict[str, Any]]:
        query = """
            SELECT id, subject_code, subject_name, exam_mode, title, started_at, submitted_at,
                   total_score, obtained_score, correct_rate, ai_used
            FROM exam_attempts
        """
        params: tuple[Any, ...] = ()
        if subject_code:
            query += " WHERE subject_code = ?"
            params = (subject_code,)
        query += " ORDER BY submitted_at DESC, started_at DESC"
        with self.connect() as conn:
            rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]

    def get_attempt(self, attempt_id: str) -> dict[str, Any] | None:
        with self.connect() as conn:
            row = conn.execute("SELECT * FROM exam_attempts WHERE id = ?", (attempt_id,)).fetchone()
        if not row:
            return None
        payload = dict(row)
        payload["blueprint"] = json.loads(payload.pop("blueprint_json"))
        payload["exam"] = json.loads(payload.pop("exam_json"))
        payload["answers"] = json.loads(payload.pop("answers_json"))
        payload["result"] = json.loads(payload.pop("result_json"))
        payload["ai_used"] = bool(payload["ai_used"])
        return payload

    def list_attempt_payloads(self, subject_code: str | None = None, limit: int | None = None) -> list[dict[str, Any]]:
        query = "SELECT * FROM exam_attempts"
        params: list[Any] = []
        if subject_code:
            query += " WHERE subject_code = ?"
            params.append(subject_code)
        query += " ORDER BY submitted_at DESC, started_at DESC"
        if limit:
            query += " LIMIT ?"
            params.append(limit)
        with self.connect() as conn:
            rows = conn.execute(query, tuple(params)).fetchall()

        payloads: list[dict[str, Any]] = []
        for row in rows:
            item = dict(row)
            item["blueprint"] = json.loads(item.pop("blueprint_json"))
            item["exam"] = json.loads(item.pop("exam_json"))
            item["answers"] = json.loads(item.pop("answers_json"))
            item["result"] = json.loads(item.pop("result_json"))
            item["ai_used"] = bool(item["ai_used"])
            payloads.append(item)
        return payloads
