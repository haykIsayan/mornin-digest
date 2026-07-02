import psycopg2
import os
from typing import Optional
from dotenv import load_dotenv
from user.domain.entity.device_token_entity import DeviceTokenEntity
from user.domain.repository.device_token_repository import DeviceTokenRepository

load_dotenv()


class PostgresDeviceTokenRepository(DeviceTokenRepository):

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
            CREATE TABLE IF NOT EXISTS device_tokens (
                user_id TEXT PRIMARY KEY,
                token TEXT NOT NULL
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()

    def save_token(self, user_id: str, token: str) -> DeviceTokenEntity:
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO device_tokens (user_id, token)
            VALUES (%s, %s)
            ON CONFLICT (user_id) DO UPDATE SET token = %s
            """,
            (user_id, token, token)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return DeviceTokenEntity(user_id=user_id, token=token)

    def get_token(self, user_id: str) -> Optional[DeviceTokenEntity]:
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT user_id, token FROM device_tokens WHERE user_id = %s",
            (user_id,)
        )
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if not row:
            return None

        return DeviceTokenEntity(user_id=row[0], token=row[1])
