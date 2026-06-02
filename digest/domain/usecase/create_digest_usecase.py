from digest.domain.entity.digest_entity import DigestEntity
from digest.domain.repository.digest_repository import DigestRepository
from digest.fetcher.articles_fetcher import ArticlesFetcher

class CreateDigestUseCase:
    def __init__(self, digest_repository: DigestRepository, articles_fetcher: ArticlesFetcher):
        self.digest_repository = digest_repository
        self.articles_fetcher = articles_fetcher

    def execute(self, userId: str, topics: list[str]) -> DigestEntity:
        articles = self.articles_fetcher.fetch_articles(topics)
        digest = self.digest_repository.create_digest(userId, articles.get('articles', []))
        return digest
