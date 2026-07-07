from fastapi import Depends, HTTPException, APIRouter

from auth.api.auth_middleware import get_current_user
from user.user_request_models import DeviceTokenRequest
from user.user_container import container as user_container

router = APIRouter(tags=["user"])

@router.post("/device-token")
def save_device_token(request: DeviceTokenRequest, user_id: str = Depends(get_current_user)):
    try:
        user_container.device_token_repository.save_token(user_id, request.token)
        return {"message": "Device token saved"}
    except Exception:
        import traceback
        print(f"Failed to save device token for {user_id}:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to save device token")
