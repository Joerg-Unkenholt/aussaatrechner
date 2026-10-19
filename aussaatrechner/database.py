from __future__ import annotations

import sqlite3
from pathlib import Path

from .models import GardenObservation


SCHEMA = """
CREATE TABLE IF NOT EXISTS observations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crop_id TEXT NOT NULL,
    sowing_date TEXT NOT NULL,
    bed_name TEXT NOT NULL,
    method TEXT NOT NULL CHECK(method IN ('outdoor', 'protected')),
    success INTEGER NOT NULL CHECK(success IN (0, 1)),
    harvest_kg REAL NULL CHECK(harvest_kg IS NULL OR harvest_kg >= 0),
    notes TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def connect(db_path: str | Path) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute(SCHEMA)
    conn.commit()
    return conn


def add_observation(conn: sqlite3.Connection, obs: GardenObservation) -> int:
    cursor = conn.execute(
        """
        INSERT INTO observations
        (crop_id, sowing_date, bed_name, method, success, harvest_kg, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            obs.crop_id,
            obs.sowing_date.isoformat(),
            obs.bed_name.strip(),
            obs.method,
            int(obs.success),
            obs.harvest_kg,
            obs.notes.strip(),
        ),
    )
    conn.commit()
    return int(cursor.lastrowid)


def list_observations(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute(
        """
        SELECT id, crop_id, sowing_date, bed_name, method, success,
               harvest_kg, notes, created_at
        FROM observations
        ORDER BY sowing_date DESC, id DESC
        """
    ).fetchall()
    return [dict(row) for row in rows]


def empirical_success(conn: sqlite3.Connection, crop_id: str) -> tuple[float | None, int]:
    row = conn.execute(
        """
        SELECT COUNT(*) AS n, SUM(success) AS successes
        FROM observations
        WHERE crop_id = ?
        """,
        (crop_id,),
    ).fetchone()

    n = int(row["n"] or 0)
    if n < 5:
        return None, n

    successes = int(row["successes"] or 0)
    return successes / n, n
