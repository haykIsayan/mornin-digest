from domain.digest.entity.digest_entity import DigestEntity
from domain.digest.repository.digest_repository import DigestRepository
from fetcher.articles_fetcher import ArticlesFetcher
from datetime import datetime

class CreateDigestUseCase:
    def __init__(self, digest_repository: DigestRepository, articles_fetcher: ArticlesFetcher):
        self.digest_repository = digest_repository
        self.articles_fetcher = articles_fetcher

    def execute(self, userId: str, topics: list[str]) -> DigestEntity:
        articles = self.articles_fetcher.fetch_articles(topics)
        digest = self.digest_repository.create_digest(userId, articles.get('articles', []))
        return digest