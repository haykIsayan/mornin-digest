class RequestOtpUseCase:

    def __init__(self, sms_sender, otp_store):
        self.sms_sender = sms_sender
        self.otp_store = otp_store

    def execute(self, phone_number: str):
        code = self.otp_store.generate_otp_code()
        self.otp_store.save_otp(phone_number, code)
        self.sms_sender.send_otp(phone_number, code)
