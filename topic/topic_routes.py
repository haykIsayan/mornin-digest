from fastapi import Depends, HTTPException, APIRouter

from auth.api.auth_middleware import get_current_user
from topic.topic_request_models import CreateTopicRequest
from topic.topic_container import container as topic_container

router = APIRouter(tags=["topics"])

@router.post("/topics", status_code=201)
def create_topic(request: CreateTopicRequest, user_id: str = Depends(get_current_user)):
    try:
        topic = topic_container.create_topic_use_case.execute(user_id, request.name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return topic

@router.delete("/topics/{topic_id}")
def delete_topic(topic_id: str, user_id: str = Depends(get_current_user)):
    try:
        topic_container.delete_topic_use_case.execute(user_id, topic_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Topic deleted"}

@router.get("/topics/defaults")
def get_default_topics():
    return topic_container.get_default_topics_use_case.execute()

@router.get("/topics")
def get_topics(user_id: str = Depends(get_current_user)):
    try:
        topics = topic_container.get_all_topics_use_case.execute(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return topics
