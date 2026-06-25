
from auth.data.sms_sender import SmsSender
from auth.data.otp_store import OtpStore
from auth.data.token_service import TokenService
from auth.domain.usecase.request_otp_usecase import RequestOtpUseCase
from auth.domain.usecase.verify_otp_usecase import VerifyOtpUseCase
from auth.data.postgres_user_repository import PostgresUserRepository
from digest.data.postgres_digest_repository import PostgresDigestRepository
from digest.domain.usecase.create_digest_usecase import CreateDigestUseCase
from digest.domain.usecase.fetch_articles_usecase import FetchArticlesUseCase
from digest.domain.usecase.get_digest_usecase import GetDigestUseCase as GetLatestDigestUseCase
from preferences.data.postgres_user_preferences_repository import PostgresUserPreferencesRepository
from preferences.domain.entity.user_preferences_entity import UserPreferencesEntity
from preferences.domain.usecase.get_preferences_usecase import GetPreferencesUseCase
from preferences.domain.usecase.save_preferences_usecase import SavePreferencesUseCase
from topic.data.postgres_topic_repository import TopicRepositoryPostgres
from topic.domain.usecase.create_topic_usecase import CreateTopicUseCase
from topic.domain.usecase.get_all_topics_usecase import GetAllTopicsUseCase
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from digest.fetcher.articles_fetcher import ArticlesFetcher


from preferences.domain.usecase.get_all_preferences_usecase import GetAllPreferencesUseCase
from scheduler.digest_scheduler import DigestScheduler

class MorninRequest(BaseModel):
    topics: List[str]

class CreateTopicRequest(BaseModel):
    name: str

class SavePreferencesRequest(BaseModel):
    delivery_time: str
    timezone: str

app = FastAPI()

digest_repository_impl = PostgresDigestRepository()
digest_repository_impl.init_db()  
topic_repository_impl = TopicRepositoryPostgres()
topic_repository_impl.init_db()

preferences_repository_impl = PostgresUserPreferencesRepository()
preferences_repository_impl.init_db()

save_preferences_use_case = SavePreferencesUseCase(preferences_repository_impl)
get_preferences_use_case = GetPreferencesUseCase(preferences_repository_impl)

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

get_all_preferences_use_case = GetAllPreferencesUseCase(preferences_repository_impl)

digest_scheduler = DigestScheduler(
    get_all_preferences_use_case=get_all_preferences_use_case,
    get_all_topics_use_case=get_all_topics_use_case,
    create_digest_use_case=create_digest_use_case
)

@app.on_event("startup")
def _start_digest_scheduler():
    digest_scheduler.start()

@app.on_event("shutdown")
def _stop_digest_scheduler():
    if digest_scheduler.scheduler.running:
        digest_scheduler.scheduler.shutdown(wait=False)

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


@app.post("/preferences/{user_id}")
def save_preferences(user_id: str, request: SavePreferencesRequest):
    try:
        preferences = UserPreferencesEntity(
            user_id=user_id,
            delivery_time=request.delivery_time,
            timezone=request.timezone
        )
        result = save_preferences_use_case.execute(preferences)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/preferences/{user_id}")
def get_preferences(user_id: str):
    result = get_preferences_use_case.execute(user_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"No preferences found for user {user_id}")
    return result


