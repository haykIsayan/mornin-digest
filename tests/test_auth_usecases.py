from unittest.mock import MagicMock

from auth.domain.entity.user_entity import UserEntity
from auth.domain.usecase.request_otp_usecase import RequestOtpUseCase
from auth.domain.usecase.verify_otp_usecase import VerifyOtpUseCase


def make_user(id="u1", phone_number="+10000000000"):
    return UserEntity(id=id, phone_number=phone_number)


class TestRequestOtpUseCase:
    def test_generates_saves_and_sends_otp(self):
        otp_sender = MagicMock()
        otp_store = MagicMock()
        otp_store.generate_otp_code.return_value = "123456"
        use_case = RequestOtpUseCase(otp_sender=otp_sender, otp_store=otp_store)

        use_case.execute("+10000000000")

        otp_store.generate_otp_code.assert_called_once()
        otp_store.save_otp.assert_called_once_with("+10000000000", "123456")
        otp_sender.send_otp.assert_called_once_with("+10000000000", "123456")


class TestVerifyOtpUseCase:
    def test_returns_none_when_otp_invalid(self):
        otp_store = MagicMock()
        otp_store.verify_otp.return_value = False
        use_case = VerifyOtpUseCase(otp_store, MagicMock(), MagicMock())

        result = use_case.execute("+10000000000", "wrong")

        assert result is None

    def test_creates_new_user_when_not_found(self):
        otp_store = MagicMock()
        otp_store.verify_otp.return_value = True
        user_repository = MagicMock()
        user_repository.find_by_phone.return_value = None
        user_repository.create_user.return_value = make_user()
        token_service = MagicMock()
        token_service.create_token.return_value = "tok123"
        use_case = VerifyOtpUseCase(otp_store, user_repository, token_service)

        result = use_case.execute("+10000000000", "123456")

        user_repository.create_user.assert_called_once_with("+10000000000")
        assert result == {"user_id": "u1", "token": "tok123"}

    def test_returns_existing_user_when_found(self):
        otp_store = MagicMock()
        otp_store.verify_otp.return_value = True
        user_repository = MagicMock()
        user_repository.find_by_phone.return_value = make_user()
        token_service = MagicMock()
        token_service.create_token.return_value = "tok123"
        use_case = VerifyOtpUseCase(otp_store, user_repository, token_service)

        result = use_case.execute("+10000000000", "123456")

        user_repository.create_user.assert_not_called()
        assert result == {"user_id": "u1", "token": "tok123"}
