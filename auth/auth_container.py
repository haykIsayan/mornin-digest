from auth.data.email_sender import EmailSender
from auth.data.otp_store import RedisOtpStore
from auth.domain.usecase.request_otp_usecase import RequestOtpUseCase
from auth.domain.usecase.verify_otp_usecase import VerifyOtpUseCase
from auth.data.postgres_user_repository import PostgresUserRepository
from auth.data.token_service import JwtTokenService

class AuthContainer:
    def __init__(self):
        self.user_repository = PostgresUserRepository()
        self.user_repository.init_db()

        otp_store = RedisOtpStore()

        self.request_otp_use_case = RequestOtpUseCase(
            otp_sender=EmailSender(),
            otp_store=otp_store
        )
        self.verify_otp_use_case = VerifyOtpUseCase(
            otp_store=otp_store,
            user_repository=self.user_repository,
            token_service=JwtTokenService()
        )

container = AuthContainer()