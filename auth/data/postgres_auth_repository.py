import psycopg2
import uuid
import os
from dotenv import load_dotenv

from auth.domain.entity.user_entity import UserEntity
from auth.domain.repository.auth_repository import AuthRepository

load_dotenv()


class PostgresAuthRepository(AuthRepository):

    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            raise RuntimeError("DATABASE_URL environment variable is required")

    def _get_connection(self):
        return psycopg2.connect(self.database_url)

    def init_db(self):
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()

    def create_user(self, email: str, password_hash: str) -> UserEntity:
        user_id = str(uuid.uuid4())
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO users (id, email, password_hash) VALUES (%s, %s, %s)",
                        (user_id, email, password_hash)
                    )
        finally:
            conn.close()

        return UserEntity(id=user_id, email=email, password_hash=password_hash)

    def get_user_by_email(self, email: str) -> UserEntity | None:
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, email, password_hash FROM users WHERE email = %s",
                    (email,)
                )
                row = cursor.fetchone()
                if not row:
                    return None
                return UserEntity(id=row[0], email=row[1], password_hash=row[2])
        finally:
            conn.close()

    def get_user_by_id(self, user_id: str) -> UserEntity | None:
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, email, password_hash FROM users WHERE id = %s",
                    (user_id,)
                )
                row = cursor.fetchone()
                if not row:
                    return None
                return UserEntity(id=row[0], email=row[1], password_hash=row[2])
        finally:
            conn.close()
