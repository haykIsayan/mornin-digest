from fastapi import Request, HTTPException
from auth.data.token_service import JwtTokenService

token_service = JwtTokenService()


def get_current_user(request: Request) -> str:
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    parts = auth_header.split(" ")

    if len(parts) != 2 or parts[0] != "Bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization format. Use: Bearer <token>")

    token = parts[1]

    user_id = token_service.verify_token(token)

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return user_id
