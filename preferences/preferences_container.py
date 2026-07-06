from preferences.data.postgres_user_preferences_repository import PostgresUserPreferencesRepository
from preferences.domain.usecase.get_all_preferences_usecase import GetAllPreferencesUseCase
from preferences.domain.usecase.get_preferences_usecase import GetPreferencesUseCase
from preferences.domain.usecase.save_preferences_usecase import SavePreferencesUseCase


class PreferencesContainer:
    def __init__(self):
        self.preferences_repository = PostgresUserPreferencesRepository()
        self.preferences_repository.init_db()

        self.save_preferences_use_case = SavePreferencesUseCase(self.preferences_repository)
        self.get_preferences_use_case = GetPreferencesUseCase(self.preferences_repository)
        self.get_all_preferences_use_case = GetAllPreferencesUseCase(self.preferences_repository)

container = PreferencesContainer()
