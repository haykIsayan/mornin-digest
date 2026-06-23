from digest.domain.entity.digest_entity import DigestEntity
from digest.domain.repository.digest_repository import DigestRepository
from digest.domain.usecase.fetch_articles_usecase import FetchArticlesUseCase

class CreateDigestUseCase:
    def __init__(self, digest_repository: DigestRepository, fetch_articles_use_case: FetchArticlesUseCase):
        self.digest_repository = digest_repository
        self.fetch_articles_use_case = fetch_articles_use_case

    def execute(self, userId: str, topics: list[str]) -> DigestEntity:
        articles = self.fetch_articles_use_case.execute(topics)
        digest = self.digest_repository.create_digest(userId, articles.get('articles', []))
        return digest
