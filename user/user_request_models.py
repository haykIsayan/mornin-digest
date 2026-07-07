from pydantic import BaseModel


class DeviceTokenRequest(BaseModel):
    token: str
