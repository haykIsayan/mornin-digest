from digest.domain.entity.digest_entity import DigestEntity
from digest.domain.repository.digest_repository import DigestRepository

class GetDigestUseCase:
    def __init__(self, digest_repository: DigestRepository):
        self.digest_repository = digest_repository

    def execute(self, userId: str) -> DigestEntity:
        digest = self.digest_repository.get_latest_digest(userId)
        return digest
