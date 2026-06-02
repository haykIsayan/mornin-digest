import uuid

from digest.domain.repository.digest_repository import DigestRepository
from digest.domain.entity.digest_entity import DigestEntity


class DigestRepositoryLocal(DigestRepository):

    def __init__(self):
        self.user_digests = {}

    def create_digest(self, userId: str, articles: list[dict]) -> DigestEntity:
        digest_id = str(uuid.uuid4())
        new_digest = DigestEntity(
            digestId=digest_id,
            userId=userId,
            articles=articles
        )
        if userId not in self.user_digests:
            self.user_digests[userId] = []
        self.user_digests[userId].append(new_digest)
        return new_digest

    def get_latest_digest(self, userId: str) -> DigestEntity:
        if userId not in self.user_digests or not self.user_digests[userId]:
            return None
        return self.user_digests[userId][-1]
