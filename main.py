
from digest.data.digest_repository_runtime import DigestRepositoryLocal
from digest.data.postgres_digest_repository import PostgresDigestRepository
from digest.domain.usecase.create_digest_usecase import CreateDigestUseCase
from digest.domain.usecase.fetch_articles_usecase import FetchArticlesUseCase
from digest.domain.usecase.get_digest_usecase import GetDigestUseCase as GetLatestDigestUseCase
from topic.data.topic_repository_runtime import TopicRepositoryRuntime
from topic.domain.usecase.create_topic_usecase import CreateTopicUseCase
from topic.domain.usecase.get_all_topics_usecase import GetAllTopicsUseCase
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from digest.fetcher.articles_fetcher import ArticlesFetcher

class MorninRequest(BaseModel):
    topics: List[str]

class CreateTopicRequest(BaseModel):
    name: str

app = FastAPI()

digest_repository_impl = PostgresDigestRepository()
digest_repository_impl.init_db()  
topic_repository_impl = TopicRepositoryRuntime()

articles_fetcher = ArticlesFetcher()
fetch_articles_use_case = FetchArticlesUseCase(articles_fetcher)

create_digest_use_case = CreateDigestUseCase(
    digest_repository_impl,
    fetch_articles_use_case
)

get_latest_digest_use_case = GetLatestDigestUseCase(
    digest_repository_impl,
)

create_topic_use_case = CreateTopicUseCase(topic_repository_impl)
get_all_topics_use_case = GetAllTopicsUseCase(topic_repository_impl)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/digest/{user_id}")
def create_digest(user_id: str, request: MorninRequest):
    try:
        digest = create_digest_use_case.execute(user_id, request.topics)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    print(digest)
    return digest

@app.get("/digest/{user_id}")
def get_digest(user_id: str):
    latest_digest = get_latest_digest_use_case.execute(user_id)
    if not latest_digest:
        raise HTTPException(status_code=404, detail=f"No digest found for user {user_id}")
    return latest_digest

@app.post("/topics/{user_id}", status_code=201)
def create_topic(user_id: str, request: CreateTopicRequest):
    try:
        topic = create_topic_use_case.execute(user_id, request.name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return topic

@app.get("/topics/{user_id}")
def get_topics(user_id: str):
    try:
        topics = get_all_topics_use_case.execute(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return topics
