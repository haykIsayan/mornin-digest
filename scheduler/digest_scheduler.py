from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from zoneinfo import ZoneInfo

from preferences.domain.usecase.get_all_preferences_usecase import GetAllPreferencesUseCase
from topic.domain.usecase.get_all_topics_usecase import GetAllTopicsUseCase
from digest.domain.usecase.create_digest_usecase import CreateDigestUseCase


class DigestScheduler:

    def __init__(
        self,
        get_all_preferences_use_case: GetAllPreferencesUseCase,
        get_all_topics_use_case: GetAllTopicsUseCase,
        create_digest_use_case: CreateDigestUseCase
    ):
        self.get_all_preferences_use_case = get_all_preferences_use_case
        self.get_all_topics_use_case = get_all_topics_use_case
        self.create_digest_use_case = create_digest_use_case
        self.scheduler = BackgroundScheduler()

    def start(self):
        self.scheduler.add_job(
            self._check_and_create_digests,
            trigger="interval",
            minutes=1
        )
        self.scheduler.start()
        print("Scheduler started — checking for digests every minute")

    def _check_and_create_digests(self):
        print("Checking for users due for a digest...")

        all_preferences = self.get_all_preferences_use_case.execute()

        for preferences in all_preferences:
            if self.is_delivery_time(preferences.delivery_time, preferences.timezone):
                print(f"It's time for {preferences.user_id}!")
                self._create_digest_for_user(preferences.user_id)

    def is_delivery_time(self, delivery_time: str, timezone: str) -> bool:
        user_now = datetime.now(ZoneInfo(timezone))
        current_time = user_now.strftime("%H:%M")
        return current_time == delivery_time

    def _create_digest_for_user(self, user_id: str):
        try:
            topics = self.get_all_topics_use_case.execute(user_id)

            if not topics:
                print(f"No topics found for {user_id}, skipping")
                return

            topic_names = [topic.name for topic in topics]

            self.create_digest_use_case.execute(user_id, topic_names)
            print(f"Digest created for {user_id}")

        except Exception:
            import traceback
            print(f"Failed to create digest for {user_id}:\n{traceback.format_exc()}")
