class VerifyOtpUseCase:

    def __init__(self, otp_store, user_repository, token_service):
        self.otp_store = otp_store
        self.user_repository = user_repository
        self.token_service = token_service

    def execute(self, phone_number: str, code: str) -> dict | None:
        if not self.otp_store.verify_otp(phone_number, code):
            return None

        user = self.user_repository.find_by_phone(phone_number)
        if not user:
            user = self.user_repository.create_user(phone_number)

        token = self.token_service.create_token(user.id)

        return {
            "user_id": user.id,
            "token": token
        }
