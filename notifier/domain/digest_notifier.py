from abc import ABC, abstractmethod

from digest.domain.entity.digest_entity import DigestEntity


class DigestNotifier(ABC):

    @abstractmethod
    def notify(self, user_id: str, digest: DigestEntity):
        pass
