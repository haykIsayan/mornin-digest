from digest.data.postgres_digest_repository import PostgresDigestRepository
from digest.domain.usecase.create_digest_usecase import CreateDigestUseCase
from digest.domain.usecase.fetch_articles_usecase import FetchArticlesUseCase
from digest.domain.usecase.get_digest_usecase import GetDigestUseCase
from digest.fetcher.articles_fetcher import ArticlesFetcher


class DigestContainer:
    def __init__(self):
        self.digest_repository = PostgresDigestRepository()
        self.digest_repository.init_db()

        articles_fetcher = ArticlesFetcher()
        fetch_articles_use_case = FetchArticlesUseCase(articles_fetcher)

        self.create_digest_use_case = CreateDigestUseCase(
            self.digest_repository,
            fetch_articles_use_case
        )
        self.get_latest_digest_use_case = GetDigestUseCase(
            self.digest_repository,
        )

container = DigestContainer()
