from twilio.rest import Client
import os
from dotenv import load_dotenv

from auth.domain.otp_sender import OtpSender

load_dotenv()


class SmsSender(OtpSender):

    def __init__(self):
        self.client = Client(
            os.getenv("TWILIO_ACCOUNT_SID"),
            os.getenv("TWILIO_AUTH_TOKEN")
        )
        self.from_number = os.getenv("TWILIO_PHONE_NUMBER")

    def send_otp(self, recipient: str, code: str):
        # self.client.messages.create(
        #     body=f"Your Mornin' code is: {code}",
        #     from_=self.from_number,
        #     to=recipient
        # )

        print(f"Sending OTP {code} to {recipient} from {self.from_number}")


