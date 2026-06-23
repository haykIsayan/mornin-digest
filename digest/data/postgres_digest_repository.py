import psycopg2
import uuid
import os
from dotenv import load_dotenv

from digest.domain.entity.digest_entity import DigestEntity
from digest.domain.repository.digest_repository import DigestRepository

load_dotenv()

class PostgresDigestRepository(DigestRepository):

    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")

    def _get_connection(self):
        return psycopg2.connect(self.database_url)
    
    def init_db(self):
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS digests (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id SERIAL PRIMARY KEY,
                digest_id TEXT NOT NULL REFERENCES digests(id),
                topic TEXT,
                title TEXT,
                summary TEXT,
                source TEXT,
                url TEXT,
                published_date TEXT
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()
        
    def create_digest(self, user_id: str, articles: list[dict]) -> DigestEntity:
        entity = DigestEntity(
            digest_id=str(uuid.uuid4()),
            user_id=user_id,
            articles=articles
        )

        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO digests (id, user_id, created_at) VALUES (%s, %s, %s)",
                        (entity.digest_id, entity.user_id, entity.created_at)
                    )
                    for article in articles:
                        cursor.execute(
                            """
                            INSERT INTO articles (digest_id, topic, title, summary, source, url, published_date)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            """,
                            (
                                entity.digest_id,
                                article.get("topic"),
                                article.get("title"),
                                article.get("summary"),
                                article.get("source"),
                                article.get("url"),
                                article.get("published_date"),
                            )
                        )
        finally:
            conn.close()

        return entity

    def get_latest_digest(self, user_id: str) -> DigestEntity | None:
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, created_at FROM digests WHERE user_id = %s ORDER BY created_at DESC LIMIT 1",
                    (user_id,)
                )
                row = cursor.fetchone()

                if not row:
                    return None

                digest_id, created_at = row

                cursor.execute(
                    "SELECT topic, title, summary, source, url, published_date FROM articles WHERE digest_id = %s",
                    (digest_id,)
                )
                articles = [
                    {
                        "topic": r[0],
                        "title": r[1],
                        "summary": r[2],
                        "source": r[3],
                        "url": r[4],
                        "published_date": r[5],
                    }
                    for r in cursor.fetchall()
                ]
        finally:
            conn.close()

        return DigestEntity(
            digest_id=digest_id,
            user_id=user_id,
            articles=articles,
            created_at=created_at
        )
