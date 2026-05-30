from domain.repository.digest_repository import DigestRepository
from fetcher.articles_fetcher import ArticlesFetcher

class CreateDigestUseCase:
    def __init__(self, digest_repository: DigestRepository, articles_fetcher: ArticlesFetcher):
        self.digest_repository = digest_repository
        self.articles_fetcher = articles_fetcher

    def execute(self, topics: list[str]):
        articles = self.articles_fetcher.fetch_articles(topics)
        digest = self.digest_repository.create_digest(articles)
        return digest