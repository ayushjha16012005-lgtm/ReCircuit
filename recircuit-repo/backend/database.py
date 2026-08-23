"""
database.py
-----------
Minimal SQLite persistence layer for the recovered-component
inventory ("digital component passport" records).

Uses only the Python standard library (sqlite3) so the backend has
no extra database dependency to install.
"""

from __future__ import annotations
import sqlite3
from pathlib import Path
from typing import Any, Dict, List

DB_PATH = Path(__file__).parent / "recircuit.db"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS inventory (
    passport_id   TEXT PRIMARY KEY,
    component_id  TEXT NOT NULL,
    component_type TEXT NOT NULL,
    measured_value TEXT NOT NULL,
    status        TEXT NOT NULL,
    grade         TEXT NOT NULL,
    source_board  TEXT NOT NULL,
    created_at    TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(_SCHEMA)
    return conn


def next_passport_id(conn: sqlite3.Connection) -> str:
    cur = conn.execute("SELECT COUNT(*) AS n FROM inventory")
    count = cur.fetchone()["n"] + 1
    return f"RC-{count:03d}"


def add_component(
    component_id: str,
    component_type: str,
    measured_value: str,
    status: str,
    grade: str,
    source_board: str,
) -> Dict[str, Any]:
    conn = get_connection()
    try:
        passport_id = next_passport_id(conn)
        conn.execute(
            """INSERT INTO inventory
               (passport_id, component_id, component_type, measured_value,
                status, grade, source_board)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (passport_id, component_id, component_type, measured_value,
             status, grade, source_board),
        )
        conn.commit()
        return dict(
            passport_id=passport_id,
            component_id=component_id,
            component_type=component_type,
            measured_value=measured_value,
            status=status,
            grade=grade,
            source_board=source_board,
        )
    finally:
        conn.close()


def list_inventory() -> List[Dict[str, Any]]:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM inventory ORDER BY created_at DESC"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def reset() -> None:
    """Wipe the inventory table. Useful for demos and tests."""
    conn = get_connection()
    try:
        conn.execute("DELETE FROM inventory")
        conn.commit()
    finally:
        conn.close()
