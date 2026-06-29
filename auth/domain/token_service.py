from abc import ABC, abstractmethod
from typing import Optional


class TokenService(ABC):

    @abstractmethod
    def create_token(self, user_id: str) -> str:
        pass

    @abstractmethod
    def verify_token(self, token: str) -> Optional[str]:
        pass
