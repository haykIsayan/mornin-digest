from auth.domain.entity.user_entity import UserEntity
from auth.domain.repository.auth_repository import AuthRepository


class GetUserUseCase:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    def execute(self, user_id: str) -> UserEntity | None:
        return self.auth_repository.get_user_by_id(user_id)
