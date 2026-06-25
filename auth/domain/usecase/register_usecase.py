import hashlib

from auth.domain.entity.user_entity import UserEntity
from auth.domain.repository.auth_repository import AuthRepository


class RegisterUseCase:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    def execute(self, email: str, password: str) -> UserEntity:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return self.auth_repository.create_user(email, password_hash)
