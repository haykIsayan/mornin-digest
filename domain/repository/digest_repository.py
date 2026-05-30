from abc import ABC, abstractmethod

class DigestRepository(ABC):

    @abstractmethod
    def create_digest(self, articles: list[dict]) -> dict:
        pass

    @abstractmethod
    def get_latest_digest(self) -> dict:
        pass

