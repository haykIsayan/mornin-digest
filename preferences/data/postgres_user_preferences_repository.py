import psycopg2
import os
from typing import Optional
from dotenv import load_dotenv

from preferences.domain.entity.user_preferences_entity import UserPreferencesEntity
from preferences.domain.repository.user_preferences_repository import UserPreferencesRepository

load_dotenv()


class PostgresUserPreferencesRepository(UserPreferencesRepository):

    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")

    def _get_connection(self):
        return psycopg2.connect(self.database_url)

    def init_db(self):
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS user_preferences (
                            user_id TEXT PRIMARY KEY,
                            delivery_time TEXT NOT NULL,
                            timezone TEXT NOT NULL
                        )
                    """)
        finally:
            conn.close()

    def save_preferences(self, preferences: UserPreferencesEntity) -> UserPreferencesEntity:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO user_preferences (user_id, delivery_time, timezone)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (user_id) DO UPDATE SET
                            delivery_time = EXCLUDED.delivery_time,
                            timezone = EXCLUDED.timezone
                        """,
                        (
                            preferences.user_id,
                            preferences.delivery_time,
                            preferences.timezone,
                        )
                    )
        finally:
            conn.close()

        return preferences

    def get_preferences(self, user_id: str) -> Optional[UserPreferencesEntity]:
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT user_id, delivery_time, timezone FROM user_preferences WHERE user_id = %s",
                    (user_id,)
                )
                row = cursor.fetchone()
        finally:
            conn.close()

        if not row:
            return None

        return UserPreferencesEntity(
            user_id=row[0],
            delivery_time=row[1],
            timezone=row[2]
        )

    def get_all_preferences(self) -> list[UserPreferencesEntity]:
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT user_id, delivery_time, timezone FROM user_preferences")
                return [
                    UserPreferencesEntity(
                        user_id=row[0],
                        delivery_time=row[1],
                        timezone=row[2]
                    )
                    for row in cursor.fetchall()
                ]
        finally:
            conn.close()
