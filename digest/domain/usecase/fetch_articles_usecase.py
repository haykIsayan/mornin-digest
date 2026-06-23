from digest.fetcher.articles_fetcher import ArticlesFetcher

class FetchArticlesUseCase:
    def __init__(self, articles_fetcher: ArticlesFetcher):
        self.articles_fetcher = articles_fetcher

    def execute(self, topics: list[str]) -> list[dict]:
        return self.articles_fetcher.fetch_articles(topics)