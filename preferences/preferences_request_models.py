from pydantic import BaseModel


class SavePreferencesRequest(BaseModel):
    delivery_time: str
    timezone: str
