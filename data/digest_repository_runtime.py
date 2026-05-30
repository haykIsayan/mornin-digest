
import uuid

from domain.repository.digest_repository import DigestRepository


class DigestRepositoryLocal(DigestRepository):

    def __init__(self):
        self.batches = []
 
    def create_digest(self, articles: list[dict]) -> dict:
        batch_id = str(uuid.uuid4())
        newBatch = (batch_id, articles)
        self.batches.append(newBatch)
        return {"batch_id": batch_id, "articles": articles}
     
    def get_latest_digest(self) -> dict:
        if not self.batches:
            return {}
        batch_id, articles = self.batches[-1]
        return {"batch_id": batch_id, "articles": articles}     
    
    
