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
from preferences.preferences_routes import router as preferences_router
from preferences.preferences_container import container as preferences_container

from scheduler.digest_scheduler import DigestScheduler

class DeviceTokenRequest(BaseModel):
    token: str

app = FastAPI()

app.include_router(auth_router, tags=["auth"])
app.include_router(topic_router, tags=["topics"])
app.include_router(digest_router, tags=["digest"])
app.include_router(preferences_router, tags=["preferences"])

device_token_repository_impl = PostgresDeviceTokenRepository()
device_token_repository_impl.init_db()

push_notifier = PushDigestNotifier(device_token_repository_impl)

digest_scheduler = DigestScheduler(
    get_all_preferences_use_case=preferences_container.get_all_preferences_use_case,
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

@app.post("/device-token")
def save_device_token(request: DeviceTokenRequest, user_id: str = Depends(get_current_user)):
    try:
        device_token_repository_impl.save_token(user_id, request.token)
        return {"message": "Device token saved"}
    except Exception:
        import traceback
        print(f"Failed to save device token for {user_id}:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to save device token")
    


