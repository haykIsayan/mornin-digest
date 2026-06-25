from unittest.mock import MagicMock, patch
from datetime import datetime
from zoneinfo import ZoneInfo

from preferences.domain.entity.user_preferences_entity import UserPreferencesEntity
from topic.domain.entity.topic_entity import TopicEntity
from scheduler.digest_scheduler import DigestScheduler


def make_scheduler(preferences=None, topics=None):
    get_all_preferences = MagicMock()
    get_all_preferences.execute.return_value = preferences or []

    get_all_topics = MagicMock()
    get_all_topics.execute.return_value = topics or []

    create_digest = MagicMock()

    scheduler = DigestScheduler(get_all_preferences, get_all_topics, create_digest)
    return scheduler, get_all_preferences, get_all_topics, create_digest


def make_preferences(user_id="u1", delivery_time="07:30", timezone="America/Los_Angeles"):
    return UserPreferencesEntity(user_id=user_id, delivery_time=delivery_time, timezone=timezone)


class TestIsDeliveryTime:
    def test_returns_true_when_current_time_matches(self):
        scheduler, _, _, _ = make_scheduler()
        fixed_time = datetime(2026, 1, 1, 7, 30, tzinfo=ZoneInfo("America/Los_Angeles"))

        with patch("scheduler.digest_scheduler.datetime") as mock_dt:
            mock_dt.now.return_value = fixed_time

            result = scheduler.is_delivery_time("07:30", "America/Los_Angeles")

        assert result is True

    def test_returns_false_when_current_time_does_not_match(self):
        scheduler, _, _, _ = make_scheduler()
        fixed_time = datetime(2026, 1, 1, 8, 0, tzinfo=ZoneInfo("America/Los_Angeles"))

        with patch("scheduler.digest_scheduler.datetime") as mock_dt:
            mock_dt.now.return_value = fixed_time

            result = scheduler.is_delivery_time("07:30", "America/Los_Angeles")

        assert result is False

    def test_respects_user_timezone(self):
        scheduler, _, _, _ = make_scheduler()
        fixed_time = datetime(2026, 1, 1, 7, 30, tzinfo=ZoneInfo("Europe/London"))

        with patch("scheduler.digest_scheduler.datetime") as mock_dt:
            mock_dt.now.return_value = fixed_time

            result = scheduler.is_delivery_time("07:30", "Europe/London")

        assert result is True


class TestCheckAndCreateDigests:
    def test_creates_digest_for_user_when_it_is_delivery_time(self):
        prefs = [make_preferences("u1", "07:30", "America/Los_Angeles")]
        scheduler, get_all_preferences, _, create_digest = make_scheduler(preferences=prefs)

        with patch.object(scheduler, "is_delivery_time", return_value=True), \
             patch.object(scheduler, "_create_digest_for_user") as mock_create:
            scheduler._check_and_create_digests()

        mock_create.assert_called_once_with("u1")

    def test_skips_user_when_it_is_not_delivery_time(self):
        prefs = [make_preferences("u1", "07:30", "America/Los_Angeles")]
        scheduler, _, _, _ = make_scheduler(preferences=prefs)

        with patch.object(scheduler, "is_delivery_time", return_value=False), \
             patch.object(scheduler, "_create_digest_for_user") as mock_create:
            scheduler._check_and_create_digests()

        mock_create.assert_not_called()

    def test_processes_multiple_users(self):
        prefs = [
            make_preferences("u1", "07:30", "America/Los_Angeles"),
            make_preferences("u2", "08:00", "Europe/London"),
        ]
        scheduler, _, _, _ = make_scheduler(preferences=prefs)

        with patch.object(scheduler, "is_delivery_time", return_value=True), \
             patch.object(scheduler, "_create_digest_for_user") as mock_create:
            scheduler._check_and_create_digests()

        assert mock_create.call_count == 2


class TestCreateDigestForUser:
    def test_creates_digest_with_topic_names(self):
        topics = [TopicEntity(id="t1", name="python"), TopicEntity(id="t2", name="rust")]
        scheduler, _, get_all_topics, create_digest = make_scheduler(topics=topics)

        scheduler._create_digest_for_user("u1")

        get_all_topics.execute.assert_called_once_with("u1")
        create_digest.execute.assert_called_once_with("u1", ["python", "rust"])

    def test_skips_digest_when_user_has_no_topics(self):
        scheduler, _, get_all_topics, create_digest = make_scheduler(topics=[])

        scheduler._create_digest_for_user("u1")

        create_digest.execute.assert_not_called()

    def test_handles_exception_without_raising(self):
        scheduler, _, get_all_topics, create_digest = make_scheduler(
            topics=[TopicEntity(id="t1", name="python")]
        )
        create_digest.execute.side_effect = Exception("Claude API error")

        scheduler._create_digest_for_user("u1")  # should not raise
