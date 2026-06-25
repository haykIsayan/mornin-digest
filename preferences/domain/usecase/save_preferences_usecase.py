from preferences.domain.entity.user_preferences_entity import UserPreferencesEntity
from preferences.domain.repository.user_preferences_repository import UserPreferencesRepository


class SavePreferencesUseCase:

    def __init__(self, repository: UserPreferencesRepository):
        self.repository = repository

    def execute(self, preferences: UserPreferencesEntity) -> UserPreferencesEntity:
        return self.repository.save_preferences(preferences)
