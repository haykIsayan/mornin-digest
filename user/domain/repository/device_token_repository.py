from abc import ABC, abstractmethod

from user.domain.entity.device_token_entity import DeviceTokenEntity


class DeviceTokenRepository(ABC):

    @abstractmethod
    def save_token(self, user_id: str, token: str) -> DeviceTokenEntity:
        pass

    @abstractmethod
    def get_token(self, user_id: str) -> DeviceTokenEntity:
        pass
