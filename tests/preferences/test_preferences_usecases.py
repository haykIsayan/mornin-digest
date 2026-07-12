from unittest.mock import MagicMock

from preferences.domain.entity.user_preferences_entity import UserPreferencesEntity
from preferences.domain.usecase.save_preferences_usecase import SavePreferencesUseCase
from preferences.domain.usecase.get_preferences_usecase import GetPreferencesUseCase
from preferences.domain.usecase.get_all_preferences_usecase import GetAllPreferencesUseCase


def make_preferences(user_id="u1", delivery_time="07:30", timezone="America/Los_Angeles"):
    return UserPreferencesEntity(user_id=user_id, delivery_time=delivery_time, timezone=timezone)


class TestSavePreferencesUseCase:
    def test_saves_and_returns_preferences(self):
        repo = MagicMock()
        preferences = make_preferences()
        repo.save_preferences.return_value = preferences
        use_case = SavePreferencesUseCase(repo)

        result = use_case.execute(preferences)

        repo.save_preferences.assert_called_once_with(preferences)
        assert result is preferences

    def test_overwrites_existing_preferences(self):
        repo = MagicMock()
        updated = make_preferences(delivery_time="09:00")
        repo.save_preferences.return_value = updated
        use_case = SavePreferencesUseCase(repo)

        result = use_case.execute(updated)

        repo.save_preferences.assert_called_once_with(updated)
        assert result.delivery_time == "09:00"


class TestGetPreferencesUseCase:
    def test_returns_preferences_for_user(self):
        repo = MagicMock()
        preferences = make_preferences()
        repo.get_preferences.return_value = preferences
        use_case = GetPreferencesUseCase(repo)

        result = use_case.execute("u1")

        repo.get_preferences.assert_called_once_with("u1")
        assert result is preferences

    def test_returns_none_when_no_preferences_exist(self):
        repo = MagicMock()
        repo.get_preferences.return_value = None
        use_case = GetPreferencesUseCase(repo)

        result = use_case.execute("u1")

        assert result is None


class TestGetAllPreferencesUseCase:
    def test_returns_all_preferences(self):
        repo = MagicMock()
        all_prefs = [make_preferences("u1"), make_preferences("u2", timezone="Europe/London")]
        repo.get_all_preferences.return_value = all_prefs
        use_case = GetAllPreferencesUseCase(repo)

        result = use_case.execute()

        repo.get_all_preferences.assert_called_once()
        assert result == all_prefs

    def test_returns_empty_list_when_no_preferences_exist(self):
        repo = MagicMock()
        repo.get_all_preferences.return_value = []
        use_case = GetAllPreferencesUseCase(repo)

        result = use_case.execute()

        assert result == []
