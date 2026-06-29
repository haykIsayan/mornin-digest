import os

import resend
from dotenv import load_dotenv

from auth.domain.otp_sender import OtpSender

load_dotenv()


class EmailSender(OtpSender):
    def __init__(self):
        api_key = os.getenv("RESEND_API_KEY")
        if not api_key:
            raise RuntimeError("RESEND_API_KEY environment variable is required")
        resend.api_key = api_key

    def send_otp(self, recipient: str, code: str):
        resend.Emails.send(
            {
                "from": "Mornin' <onboarding@resend.dev>",
                "to": [recipient],
                "subject": "Your Mornin' code",
                "html": f"<p>Your verification code is: <strong>{code}</strong></p>",
            }
        )
        print(f"Sending OTP to {recipient}")
