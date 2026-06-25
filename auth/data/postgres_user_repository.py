import psycopg2
import uuid
import os
from dotenv import load_dotenv
from auth.domain.entity.user_entity import UserEntity
from auth.domain.repository.user_repository import UserRepository

load_dotenv()


class PostgresUserRepository(UserRepository):

    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")

    def _get_connection(self):
        return psycopg2.connect(self.database_url)

    def init_db(self):
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                phone_number TEXT UNIQUE NOT NULL,
                name TEXT
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()

    def find_by_phone(self, phone_number: str) -> UserEntity | None:
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, phone_number, name FROM users WHERE phone_number = %s",
            (phone_number,)
        )
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if not row:
            return None

        return UserEntity(id=row[0], phone_number=row[1], name=row[2])

    def create_user(self, phone_number: str) -> UserEntity:
        conn = self._get_connection()
        cursor = conn.cursor()

        user_id = str(uuid.uuid4())

        cursor.execute(
            "INSERT INTO users (id, phone_number) VALUES (%s, %s)",
            (user_id, phone_number)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return UserEntity(id=user_id, phone_number=phone_number)
