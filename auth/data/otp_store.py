import random
import redis
import os
from dotenv import load_dotenv

load_dotenv()


class OtpStore:

    def __init__(self):
        self.redis = redis.from_url(os.getenv("UPSTASH_REDIS_URL"))

    def generate_otp_code(self) -> str:
        return str(random.randint(100000, 999999))

    def save_otp(self, phone_number: str, code: str):
        self.redis.setex(
            name=f"otp:{phone_number}",
            time=300,
            value=code
        )

    def verify_otp(self, phone_number: str, code: str) -> bool:
        stored_code = self.redis.get(f"otp:{phone_number}")

        if not stored_code:
            return False

        if stored_code.decode("utf-8") == code:
            self.redis.delete(f"otp:{phone_number}")
            return True

        return False
