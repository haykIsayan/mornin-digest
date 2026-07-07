from notifier.data.push_digest_notifier import PushDigestNotifier
from scheduler.digest_scheduler import DigestScheduler
from topic.topic_container import container as topic_container
from digest.digest_container import container as digest_container
from preferences.preferences_container import container as preferences_container
from user.user_container import container as user_container


class SchedulerContainer:
    def __init__(self):
        push_notifier = PushDigestNotifier(user_container.device_token_repository)

        self.digest_scheduler = DigestScheduler(
            get_all_preferences_use_case=preferences_container.get_all_preferences_use_case,
            get_all_topics_use_case=topic_container.get_all_topics_use_case,
            create_digest_use_case=digest_container.create_digest_use_case,
            digest_notifier=push_notifier
        )

container = SchedulerContainer()
