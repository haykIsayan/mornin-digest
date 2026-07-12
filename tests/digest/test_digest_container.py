from digest.digest_container import container as digest_container
from digest.data.digest_repository_runtime import DigestRepositoryRuntime
from digest.domain.usecase.create_digest_usecase import CreateDigestUseCase
from digest.domain.usecase.get_digest_usecase import GetDigestUseCase
from digest.domain.usecase.fetch_articles_usecase import FetchArticlesUseCase
from unittest.mock import MagicMock


def setup_test_digest_container():
    # --- Digest ---
    test_digest_repo = DigestRepositoryRuntime()

    # Mock the articles fetcher so it doesn't call Claude
    mock_fetcher = MagicMock()
    mock_fetcher.execute.return_value = {
        "articles": [
            {
                "topic": "technology",
                "title": "Test Article",
                "summary": "A test summary",
                "source": "Test Source",
                "url": "https://example.com",
                "published_date": "2026-07-07"
            }
        ]
    }

    digest_container.create_digest_use_case = CreateDigestUseCase(
        test_digest_repo,
        mock_fetcher
    )
    digest_container.get_latest_digest_use_case = GetDigestUseCase(
        test_digest_repo
    )

setup_test_digest_container()