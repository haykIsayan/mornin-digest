from abc import ABC, abstractmethod


class OtpSender(ABC):

    @abstractmethod
    def send_otp(self, recipient: str, code: str):
        pass
