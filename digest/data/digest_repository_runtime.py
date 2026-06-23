import uuid

from digest.domain.repository.digest_repository import DigestRepository
from digest.domain.entity.digest_entity import DigestEntity


class DigestRepositoryLocal(DigestRepository):

    def __init__(self):
        self.user_digests = {}

    def create_digest(self, user_id: str, articles: list[dict]) -> DigestEntity:
        digest_id = str(uuid.uuid4())
        new_digest = DigestEntity(
            digest_id=digest_id,
            user_id=user_id,
            articles=articles
        )
        if user_id not in self.user_digests:
            self.user_digests[user_id] = []
        self.user_digests[user_id].append(new_digest)
        return new_digest

    def get_latest_digest(self, user_id: str) -> DigestEntity:
        if user_id not in self.user_digests or not self.user_digests[user_id]:
            return None
        return self.user_digests[user_id][-1]
