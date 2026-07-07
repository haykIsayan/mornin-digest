import uuid

from auth.domain.repository.user_repository import UserRepository
from auth.domain.entity.user_entity import UserEntity


class UserRepositoryRuntime(UserRepository):

    def __init__(self):
        self.users_by_phone = {}

    def find_by_phone(self, phone_number: str) -> UserEntity:
        return self.users_by_phone.get(phone_number)

    def create_user(self, phone_number: str) -> UserEntity:
        user = UserEntity(id=str(uuid.uuid4()), phone_number=phone_number)
        self.users_by_phone[phone_number] = user
        return user
