from user.data.postgres_device_token_repository import PostgresDeviceTokenRepository


class UserContainer:
    def __init__(self):
        self.device_token_repository = PostgresDeviceTokenRepository()
        self.device_token_repository.init_db()

container = UserContainer()
