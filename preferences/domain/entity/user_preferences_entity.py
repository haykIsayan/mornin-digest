class UserPreferencesEntity:
    def __init__(self, user_id: str, delivery_time: str, timezone: str):
        self.user_id = user_id
        self.delivery_time = delivery_time  # e.g. "07:30"
        self.timezone = timezone  # e.g. "America/Los_Angeles"
