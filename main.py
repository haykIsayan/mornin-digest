
from data.digest_repository_runtime import DigestRepositoryLocal
from domain.usecase.create_digest_usecase import CreateDigestUseCase
from domain.usecase.get_digest_usecase import GetDigestUseCase as GetLatestDigestUseCase
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fetcher.articles_fetcher import ArticlesFetcher

class MorninRequest(BaseModel):
    topics: List[str]

app = FastAPI()

digest_repository_impl = DigestRepositoryLocal()

articles_fetcher = ArticlesFetcher()

create_digest_use_case = CreateDigestUseCase(
    digest_repository_impl, 
    articles_fetcher
)

get_latest_digest_use_case = GetLatestDigestUseCase(
    digest_repository_impl,
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/mornin/{user_id}")
def mornin(user_id: str, request: MorninRequest):
    try:
        digest = create_digest_use_case.execute(user_id, request.topics)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    print(digest)
    return digest

@app.get("/digest/{user_id}")
def digest(user_id: str):
    latest_digest = get_latest_digest_use_case.execute(user_id)
    if not latest_digest:
        raise HTTPException(status_code=404, detail=f"No digest found for user {user_id}")
    return latest_digest
