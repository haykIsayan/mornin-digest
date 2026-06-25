from abc import ABC, abstractmethod

from auth.domain.entity.user_entity import UserEntity


class AuthRepository(ABC):

    @abstractmethod
    def create_user(self, email: str, password_hash: str) -> UserEntity:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> UserEntity | None:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> UserEntity | None:
        pass
