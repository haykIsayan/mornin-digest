from typing import Optional

from auth.domain.otp_store import OtpStore
from auth.domain.repository.user_repository import UserRepository
from auth.domain.token_service import TokenService


class VerifyOtpUseCase:

    def __init__(self, otp_store: OtpStore, user_repository: UserRepository, token_service: TokenService):
        self.otp_store = otp_store
        self.user_repository = user_repository
        self.token_service = token_service

    def execute(self, recipient: str, code: str) -> Optional[dict]:
        if not self.otp_store.verify_otp(recipient, code):
            return None

        user = self.user_repository.find_by_phone(recipient)
        if not user:
            user = self.user_repository.create_user(recipient)

        token = self.token_service.create_token(user.id)

        return {
            "user_id": user.id,
            "token": token
        }
