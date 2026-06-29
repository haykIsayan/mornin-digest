from auth.domain.otp_sender import OtpSender


class RequestOtpUseCase:

    def __init__(self, otp_sender: OtpSender, otp_store):
        self.otp_sender = otp_sender
        self.otp_store = otp_store

    def execute(self, recipient: str):
        code = self.otp_store.generate_otp_code()
        self.otp_store.save_otp(recipient, code)
        self.otp_sender.send_otp(recipient, code)
