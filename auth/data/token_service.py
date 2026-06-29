import jwt
import os
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv

from auth.domain.token_service import TokenService

load_dotenv()

_JWT_ALGORITHM = "HS256"


class JwtTokenService(TokenService):

    def __init__(self):
        self.secret = os.getenv("JWT_SECRET")

    def create_token(self, user_id: str) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.now() + timedelta(days=30)
        }
        return jwt.encode(payload, self.secret, algorithm=_JWT_ALGORITHM)

    def verify_token(self, token: str) -> Optional[str]:
        try:
            payload = jwt.decode(token, self.secret, algorithms=[_JWT_ALGORITHM])
            return payload["user_id"]
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
