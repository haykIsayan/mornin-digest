from digest.domain.entity.digest_entity import DigestEntity
from notifier.domain.digest_notifier import DigestNotifier


class EmailDigestNotifier(DigestNotifier):

    def notify(self, user_id: str, digest: DigestEntity):
        print(f"Sending email digest to user {user_id}")
