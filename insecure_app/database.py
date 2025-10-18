import sqlite3
from typing import Iterable, Optional

from flask import current_app, g


def get_connection() -> sqlite3.Connection:

    if "db_conn" not in g:
        database_path = current_app.config["DATABASE_PATH"]
        conn = sqlite3.connect(database_path)
        conn.row_factory = sqlite3.Row
        g.db_conn = conn
    return g.db_conn


def close_connection(_: Optional[BaseException] = None) -> None:
    conn = g.pop("db_conn", None)
    if conn is not None:
        conn.close()


def _log_query(query: str) -> None:
    if not hasattr(g, "sql_queries"):
        g.sql_queries = []
    g.sql_queries.append(query)


def unsafe_fetch_all(query: str) -> Iterable[sqlite3.Row]:

    _log_query(query)
    cursor = get_connection().execute(query)
    return cursor.fetchall()


def unsafe_fetch_one(query: str) -> Optional[sqlite3.Row]:
    _log_query(query)
    cursor = get_connection().execute(query)
    return cursor.fetchone()


def get_query_log() -> Iterable[str]:
    if not hasattr(g, "sql_queries"):
        return []
    return g.sql_queries
