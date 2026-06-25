import uuid

from auth.domain.entity.user_entity import UserEntity
from auth.domain.repository.auth_repository import AuthRepository


class AuthRepositoryRuntime(AuthRepository):

    def __init__(self):
        self.users: dict[str, UserEntity] = {}

    def create_user(self, email: str, password_hash: str) -> UserEntity:
        user_id = str(uuid.uuid4())
        user = UserEntity(id=user_id, email=email, password_hash=password_hash)
        self.users[user_id] = user
        return user

    def get_user_by_email(self, email: str) -> UserEntity | None:
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    def get_user_by_id(self, user_id: str) -> UserEntity | None:
        return self.users.get(user_id)
