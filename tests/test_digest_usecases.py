from unittest.mock import MagicMock
from datetime import datetime

from digest.domain.entity.digest_entity import DigestEntity
from digest.domain.usecase.create_digest_usecase import CreateDigestUseCase
from digest.domain.usecase.fetch_articles_usecase import FetchArticlesUseCase
from digest.domain.usecase.get_digest_usecase import GetDigestUseCase


def make_digest(digest_id="d1", user_id="u1", articles=None):
    return DigestEntity(
        digest_id=digest_id,
        user_id=user_id,
        articles=articles or [],
        created_at=datetime(2026, 1, 1),
    )


class TestFetchArticlesUseCase:
    def test_delegates_to_fetcher(self):
        fetcher = MagicMock()
        fetcher.fetch_articles.return_value = {"articles": [{"title": "A"}]}
        use_case = FetchArticlesUseCase(fetcher)

        result = use_case.execute(["python"])

        fetcher.fetch_articles.assert_called_once_with(["python"])
        assert result == {"articles": [{"title": "A"}]}


class TestCreateDigestUseCase:
    def test_fetches_articles_and_saves_digest(self):
        fetch_articles = MagicMock()
        fetch_articles.execute.return_value = {"articles": [{"title": "A"}]}
        repo = MagicMock()
        repo.create_digest.return_value = make_digest(articles=[{"title": "A"}])
        use_case = CreateDigestUseCase(repo, fetch_articles)

        result = use_case.execute("u1", ["python"])

        fetch_articles.execute.assert_called_once_with(["python"])
        repo.create_digest.assert_called_once_with("u1", [{"title": "A"}])
        assert result.user_id == "u1"
        assert result.articles == [{"title": "A"}]

    def test_passes_empty_articles_when_fetcher_returns_none(self):
        fetch_articles = MagicMock()
        fetch_articles.execute.return_value = {}
        repo = MagicMock()
        repo.create_digest.return_value = make_digest()
        use_case = CreateDigestUseCase(repo, fetch_articles)

        use_case.execute("u1", ["python"])

        repo.create_digest.assert_called_once_with("u1", [])


class TestGetDigestUseCase:
    def test_returns_latest_digest(self):
        repo = MagicMock()
        digest = make_digest()
        repo.get_latest_digest.return_value = digest
        use_case = GetDigestUseCase(repo)

        result = use_case.execute("u1")

        repo.get_latest_digest.assert_called_once_with("u1")
        assert result is digest

    def test_returns_none_when_no_digest_exists(self):
        repo = MagicMock()
        repo.get_latest_digest.return_value = None
        use_case = GetDigestUseCase(repo)

        result = use_case.execute("u1")

        assert result is None
