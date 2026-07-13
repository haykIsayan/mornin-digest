import uuid

from digest.domain.repository.digest_repository import DigestRepository
from digest.domain.entity.article_entity import ArticleEntity
from digest.domain.entity.digest_entity import DigestEntity


class DigestRepositoryLocal(DigestRepository):

    def __init__(self):
        self.user_digests = {}

    def create_digest(self, user_id: str, articles: list[dict]) -> DigestEntity:
        digest_id = str(uuid.uuid4())
        article_entities = [
            ArticleEntity(
                article_id=str(uuid.uuid4()),
                topic=article.get("topic"),
                title=article.get("title"),
                summary=article.get("summary"),
                source=article.get("source"),
                url=article.get("url"),
                published_date=article.get("published_date"),
            )
            for article in articles
        ]
        new_digest = DigestEntity(
            digest_id=digest_id,
            user_id=user_id,
            articles=article_entities
        )
        if user_id not in self.user_digests:
            self.user_digests[user_id] = []
        self.user_digests[user_id].append(new_digest)
        return new_digest

    def get_latest_digest(self, user_id: str) -> DigestEntity:
        if user_id not in self.user_digests or not self.user_digests[user_id]:
            return None
        return self.user_digests[user_id][-1]
