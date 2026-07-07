from fastapi import FastAPI
from contextlib import asynccontextmanager
from auth.auth_routes import router as auth_router
from topic.topic_routes import router as topic_router
from digest.digest_routes import router as digest_router
from preferences.preferences_routes import router as preferences_router
from user.user_routes import router as user_router
from scheduler.scheduler_container import container as scheduler_container

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    scheduler_container.digest_scheduler.start()
    yield
    # Shutdown
    if scheduler_container.digest_scheduler.scheduler.running:
        scheduler_container.digest_scheduler.scheduler.shutdown(wait=False)

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, tags=["auth"])
app.include_router(topic_router, tags=["topics"])
app.include_router(digest_router, tags=["digest"])
app.include_router(preferences_router, tags=["preferences"])
app.include_router(user_router, tags=["user"])

@app.get("/health")
def health():
    return {"status": "ok"}

