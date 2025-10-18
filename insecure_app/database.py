"""Database helpers with parameterized execution."""

import sqlite3
from typing import Optional, Sequence

from flask import current_app, g


def get_connection() -> sqlite3.Connection:
    """Return per-request SQLite connection."""
    if "db_conn" not in g:
        database_path = current_app.config["DATABASE_PATH"]
        conn = sqlite3.connect(database_path)
        conn.row_factory = sqlite3.Row
        g.db_conn = conn
    return g.db_conn


def close_connection(_: Optional[BaseException] = None) -> None:
    """Close cached connection."""
    conn = g.pop("db_conn", None)
    if conn is not None:
        conn.close()


def _log_query(query: str, params: Sequence[object]) -> None:
    """Record SQL and parameters."""
    if not hasattr(g, "sql_queries"):
        g.sql_queries = []
    g.sql_queries.append(f"{query} params={tuple(params)}")


def execute_safe(
    query: str,
    params: Optional[Sequence[object]] = None,
    *,
    fetchone: bool = False,
):
    """Run a parameterized query and return rows."""
    values: Sequence[object] = params or ()
    _log_query(query, values)
    cursor = get_connection().execute(query, values)
    if fetchone:
        return cursor.fetchone()
    return cursor.fetchall()


def get_query_log():
    """Expose SQL log."""
    if not hasattr(g, "sql_queries"):
        return []
    return g.sql_queries
