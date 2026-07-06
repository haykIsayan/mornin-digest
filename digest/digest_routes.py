from fastapi import Depends, HTTPException, APIRouter

from auth.api.auth_middleware import get_current_user
from digest.digest_request_models import MorninRequest
from digest.digest_container import container as digest_container

router = APIRouter(tags=["digest"])

@router.post("/digest")
def create_digest(request: MorninRequest, user_id: str = Depends(get_current_user)):
    try:
        digest = digest_container.create_digest_use_case.execute(user_id, request.topics)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    print(digest)
    return digest

@router.get("/digest")
def get_digest(user_id: str = Depends(get_current_user)):
    latest_digest = digest_container.get_latest_digest_use_case.execute(user_id)
    if not latest_digest:
        raise HTTPException(status_code=404, detail=f"No digest found for user {user_id}")
    return latest_digest
