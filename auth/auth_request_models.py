from pydantic import BaseModel

class RequestOtpRequest(BaseModel):
    otp_recipient: str

class VerifyOtpRequest(BaseModel):
    otp_recipient: str
    code: str