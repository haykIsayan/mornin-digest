from abc import ABC, abstractmethod

from digest.domain.entity.digest_entity import DigestEntity

class DigestRepository(ABC):

    @abstractmethod
    def create_digest(self, userId: str, articles: list[dict]) -> DigestEntity:
        pass

    @abstractmethod
    def get_latest_digest(self, userId: str) -> DigestEntity:
        pass
