from abc import ABC, abstractmethod
from auth.domain.entity.user_entity import UserEntity


class UserRepository(ABC):

    @abstractmethod
    def find_by_phone(self, phone_number: str) -> UserEntity | None:
        pass

    @abstractmethod
    def create_user(self, phone_number: str) -> UserEntity:
        pass