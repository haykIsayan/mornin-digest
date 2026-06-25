from abc import ABC, abstractmethod
from typing import Optional

from preferences.domain.entity.user_preferences_entity import UserPreferencesEntity


class UserPreferencesRepository(ABC):

    @abstractmethod
    def save_preferences(self, preferences: UserPreferencesEntity) -> UserPreferencesEntity:
        pass

    @abstractmethod
    def get_preferences(self, user_id: str) -> Optional[UserPreferencesEntity]:
        pass

    @abstractmethod
    def get_all_preferences(self) -> list[UserPreferencesEntity]:
        pass
