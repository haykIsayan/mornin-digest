from auth.auth_container import container as auth_container
from auth.data.user_repository_runtime import UserRepositoryRuntime
from auth.data.token_service import JwtTokenService
from auth.domain.usecase.request_otp_usecase import RequestOtpUseCase
from auth.domain.usecase.verify_otp_usecase import VerifyOtpUseCase
from unittest.mock import MagicMock

TEST_OTP_CODE = "123456"


def setup_test_auth_container():
    # --- Auth ---
    test_user_repo = UserRepositoryRuntime()

    # Mock the OTP store/sender so tests don't hit Redis or send real emails
    mock_otp_store = MagicMock()
    mock_otp_store.generate_otp_code.return_value = TEST_OTP_CODE
    mock_otp_store.verify_otp.side_effect = lambda recipient, code: code == TEST_OTP_CODE

    mock_otp_sender = MagicMock()

    auth_container.request_otp_use_case = RequestOtpUseCase(
        otp_sender=mock_otp_sender,
        otp_store=mock_otp_store
    )
    auth_container.verify_otp_use_case = VerifyOtpUseCase(
        otp_store=mock_otp_store,
        user_repository=test_user_repo,
        token_service=JwtTokenService()
    )

setup_test_auth_container()
