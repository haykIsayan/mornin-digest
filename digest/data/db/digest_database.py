import sqlite3
import uuid
from datetime import datetime

DATABASE_PATH = "mornin.db"

def _get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = _get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_id TEXT NOT NULL,
            topic TEXT,
            title TEXT,
            summary TEXT,
            source TEXT,
            url TEXT,
            published_date TEXT,
            fetched_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_articles(articles: list[dict]) -> str:
    batch_id = str(uuid.uuid4())
    fetched_at = datetime.now().isoformat()
    conn = _get_connection()

    for article in articles:
        conn.execute(
            """
            INSERT INTO articles (batch_id, topic, title, summary, source, url, published_date, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                batch_id,
                article.get("topic"),
                article.get("title"),
                article.get("summary"),
                article.get("source"),
                article.get("url"),
                article.get("published_date"),
                fetched_at,
            ),
        )

    conn.commit()
    conn.close()
    return batch_id

def get_latest_batch() -> list[dict]:
    conn = _get_connection()

    row = conn.execute(
        "SELECT batch_id FROM articles ORDER BY fetched_at DESC LIMIT 1"
    ).fetchone()

    if not row:
        conn.close()
        return []

    rows = conn.execute(
        "SELECT topic, title, summary, source, url, published_date, fetched_at FROM articles WHERE batch_id = ?",
        (row["batch_id"],),
    ).fetchall()

    conn.close()
    return [dict(r) for r in rows]
