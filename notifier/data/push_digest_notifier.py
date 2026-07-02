from digest.domain.entity.digest_entity import DigestEntity
from notifier.domain.digest_notifier import DigestNotifier

import firebase_admin
from firebase_admin import credentials, messaging
import os
from dotenv import load_dotenv

load_dotenv()

class PushDigestNotifier(DigestNotifier):

    def __init__(self, device_token_repository):
        self.device_token_repository = device_token_repository
        credentials_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
        if not credentials_path:
            raise RuntimeError("FIREBASE_CREDENTIALS_PATH environment variable is required")
        if not os.path.exists(credentials_path):
            raise RuntimeError(f"Firebase credentials file not found at {credentials_path}")

        cred = credentials.Certificate(credentials_path)
        try:
            firebase_admin.get_app()
        except ValueError:
            firebase_admin.initialize_app(cred)

    def notify(self, user_id: str, digest: DigestEntity):
        device_token = self.device_token_repository.get_token(user_id)
        if not device_token:
            print(f"No device token found for user {user_id}")
            return
        message = messaging.Message(
            notification=messaging.Notification(
                title="Your Mornin' digest is ready ☀️",
                body=f"{len(digest.articles)} fresh articles waiting for you"
            ),
            data={
                "type": "digest",
                "digest_id": digest.id
            },
            token=device_token.token
        )
        messaging.send(message)
