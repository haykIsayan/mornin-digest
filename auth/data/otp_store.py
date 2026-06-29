import random
import redis
import os
from dotenv import load_dotenv

from auth.domain.otp_store import OtpStore

load_dotenv()


class RedisOtpStore(OtpStore):

    def __init__(self):
        redis_url = os.getenv("UPSTASH_REDIS_URL")
        if not redis_url:
            raise RuntimeError("UPSTASH_REDIS_URL environment variable is required")
        self.redis = redis.from_url(redis_url)

    def generate_otp_code(self) -> str:
        return str(random.randint(100000, 999999))

    def save_otp(self, recipient: str, code: str):
        self.redis.setex(
            name=f"otp:{recipient}",
            time=300,
            value=code
        )

    def verify_otp(self, recipient: str, code: str) -> bool:
        stored_code = self.redis.get(f"otp:{recipient}")

        if not stored_code:
            return False

        if stored_code.decode("utf-8") == code:
            self.redis.delete(f"otp:{recipient}")
            return True

        return False
