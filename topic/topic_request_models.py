from pydantic import BaseModel

class CreateTopicRequest(BaseModel):
    name: str
