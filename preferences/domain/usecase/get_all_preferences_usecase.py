from preferences.domain.entity.user_preferences_entity import UserPreferencesEntity
from preferences.domain.repository.user_preferences_repository import UserPreferencesRepository


class GetAllPreferencesUseCase:

    def __init__(self, repository: UserPreferencesRepository):
        self.repository = repository

    def execute(self) -> list[UserPreferencesEntity]:
        return self.repository.get_all_preferences()
