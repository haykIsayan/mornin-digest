from abc import ABC, abstractmethod


class OtpStore(ABC):

    @abstractmethod
    def generate_otp_code(self) -> str:
        pass

    @abstractmethod
    def save_otp(self, recipient: str, code: str):
        pass

    @abstractmethod
    def verify_otp(self, recipient: str, code: str) -> bool:
        pass
