import hashlib

from auth.domain.entity.user_entity import UserEntity
from auth.domain.repository.auth_repository import AuthRepository


class LoginUseCase:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    def execute(self, email: str, password: str) -> UserEntity | None:
        user = self.auth_repository.get_user_by_email(email)
        if not user:
            return None
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if user.password_hash != password_hash:
            return None
        return user
