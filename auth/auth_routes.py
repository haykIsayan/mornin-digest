from fastapi import FastAPI, Depends, HTTPException, APIRouter
# from auth_request_models import RequestOtpRequest, VerifyOtpRequest
from auth.auth_request_models import RequestOtpRequest, VerifyOtpRequest
from auth.auth_container import auth_container

router = APIRouter(tags=["auth"])

@router.post("/auth/request-otp")
def request_otp(request: RequestOtpRequest):
    try:
        auth_container.request_otp_use_case.execute(request.otp_recipient)
        return {"message": "OTP sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/auth/verify-otp")
def verify_otp(request: VerifyOtpRequest):
    result = auth_container.verify_otp_use_case.execute(request.otp_recipient, request.code)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid or expired code")
    return result