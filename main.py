from preferences.data.postgres_user_preferences_repository import PostgresUserPreferencesRepository
from preferences.domain.entity.user_preferences_entity import UserPreferencesEntity
from preferences.domain.usecase.get_preferences_usecase import GetPreferencesUseCase
from preferences.domain.usecase.save_preferences_usecase import SavePreferencesUseCase
from user.data.postgres_device_token_repository import PostgresDeviceTokenRepository
from notifier.data.push_digest_notifier import PushDigestNotifier
from fastapi import FastAPI, HTTPException, Depends
from auth.api.auth_middleware import get_current_user
from pydantic import BaseModel

from auth.auth_routes import router as auth_router
from topic.topic_routes import router as topic_router
from topic.topic_container import container as topic_container
from digest.digest_routes import router as digest_router
from digest.digest_container import container as digest_container


from preferences.domain.usecase.get_all_preferences_usecase import GetAllPreferencesUseCase
from scheduler.digest_scheduler import DigestScheduler

class SavePreferencesRequest(BaseModel):
    delivery_time: str
    timezone: str

class DeviceTokenRequest(BaseModel):
    token: str

app = FastAPI()

app.include_router(auth_router, tags=["auth"])
app.include_router(topic_router, tags=["topics"])
app.include_router(digest_router, tags=["digest"])

preferences_repository_impl = PostgresUserPreferencesRepository()
preferences_repository_impl.init_db()

device_token_repository_impl = PostgresDeviceTokenRepository()
device_token_repository_impl.init_db()

save_preferences_use_case = SavePreferencesUseCase(preferences_repository_impl)
get_preferences_use_case = GetPreferencesUseCase(preferences_repository_impl)

get_all_preferences_use_case = GetAllPreferencesUseCase(preferences_repository_impl)

push_notifier = PushDigestNotifier(device_token_repository_impl)

digest_scheduler = DigestScheduler(
    get_all_preferences_use_case=get_all_preferences_use_case,
    get_all_topics_use_case=topic_container.get_all_topics_use_case,
    create_digest_use_case=digest_container.create_digest_use_case,
    digest_notifier=push_notifier
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

@app.post("/preferences")
def save_preferences(request: SavePreferencesRequest, user_id: str = Depends(get_current_user)):
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


@app.get("/preferences")
def get_preferences(user_id: str = Depends(get_current_user)):
    result = get_preferences_use_case.execute(user_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"No preferences found for user {user_id}")
    return result


@app.post("/device-token")
def save_device_token(request: DeviceTokenRequest, user_id: str = Depends(get_current_user)):
    try:
        device_token_repository_impl.save_token(user_id, request.token)
        return {"message": "Device token saved"}
    except Exception:
        import traceback
        print(f"Failed to save device token for {user_id}:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to save device token")
    


