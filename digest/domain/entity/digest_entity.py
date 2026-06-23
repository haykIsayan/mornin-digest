from datetime import datetime

class DigestEntity:
    def __init__(self, digest_id: str, user_id: str, articles: list[dict], created_at: datetime = None):
        self.digest_id = digest_id
        self.user_id = user_id
        self.articles = articles
        self.created_at = created_at or datetime.now()
