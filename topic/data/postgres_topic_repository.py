import psycopg2
import uuid
import os
from dotenv import load_dotenv
from topic.domain.entity.topic_entity import TopicEntity
from topic.domain.repository.topic_repository import TopicRepository

load_dotenv()

class TopicRepositoryPostgres(TopicRepository):

    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")

    def _get_connection(self):
        return psycopg2.connect(self.database_url)
    
    def init_db(self):
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS topics (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                name TEXT NOT NULL
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()

    def create_topic(self, user_id: str, name: str) -> TopicEntity:
        conn = self._get_connection()
        cursor = conn.cursor()

        topic_id = str(uuid.uuid4())

        cursor.execute(
            "INSERT INTO topics (id, user_id, name) VALUES (%s, %s, %s)",
            (topic_id, user_id, name)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return TopicEntity(id=topic_id, name=name)
    
    def get_all_topics(self, user_id: str) -> list[TopicEntity]:
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, name FROM topics WHERE user_id = %s",
            (user_id,)
        )

        topics = [
            TopicEntity(id=row[0], name=row[1])
            for row in cursor.fetchall()
        ]

        cursor.close()
        conn.close()

        return topics