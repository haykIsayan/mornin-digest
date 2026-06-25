from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()


class SmsSender:

    def __init__(self):
        self.client = Client(
            os.getenv("TWILIO_ACCOUNT_SID"),
            os.getenv("TWILIO_AUTH_TOKEN")
        )
        self.from_number = os.getenv("TWILIO_PHONE_NUMBER")

    def send_otp(self, phone_number: str, code: str):
        self.client.messages.create(
            body=f"Your Mornin' code is: {code}",
            from_=self.from_number,
            to=phone_number
        )
