from fastapi import Depends, HTTPException, APIRouter

from auth.api.auth_middleware import get_current_user
from preferences.domain.entity.user_preferences_entity import UserPreferencesEntity
from preferences.preferences_request_models import SavePreferencesRequest
from preferences.preferences_container import container as preferences_container

router = APIRouter(tags=["preferences"])

@router.post("/preferences")
def save_preferences(request: SavePreferencesRequest, user_id: str = Depends(get_current_user)):
    try:
        preferences = UserPreferencesEntity(
            user_id=user_id,
            delivery_time=request.delivery_time,
            timezone=request.timezone
        )
        result = preferences_container.save_preferences_use_case.execute(preferences)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/preferences")
def get_preferences(user_id: str = Depends(get_current_user)):
    result = preferences_container.get_preferences_use_case.execute(user_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"No preferences found for user {user_id}")
    return result
