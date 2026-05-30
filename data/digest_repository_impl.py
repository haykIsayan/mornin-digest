
from domain.repository.digest_repository import DigestRepository
from data.db.digest_database import get_latest_batch


class DigestRepositoryImpl(DigestRepository):
    def __init__(self):

        pass

    def create_digest(self, articles: list[dict]) -> dict:
        
        return {}
    
    def get_latest_digest(self) -> dict:
        batch = get_latest_batch()
        if batch:
            return {
                "digest": batch
            }
        return {}
    
