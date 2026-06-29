class UserEntity:
    def __init__(self, id: str, phone_number: str, name: str = None):
        self.id = id
        self.phone_number = phone_number
        self.name = name
