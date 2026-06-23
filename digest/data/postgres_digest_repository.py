import psycopg2
import uuid
import os
from dotenv import load_dotenv

from digest.domain.repository.digest_repository import DigestRepository

load_dotenv()

class PostgresDigestRepository(DigestRepository):

    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")

    def _get_connection(self):
        return psycopg2.connect(self.database_url)