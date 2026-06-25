from typing import Optional

from preferences.domain.entity.user_preferences_entity import UserPreferencesEntity
from preferences.domain.repository.user_preferences_repository import UserPreferencesRepository


class GetPreferencesUseCase:

    def __init__(self, repository: UserPreferencesRepository):
        self.repository = repository

    def execute(self, user_id: str) -> Optional[UserPreferencesEntity]:
        return self.repository.get_preferences(user_id)
