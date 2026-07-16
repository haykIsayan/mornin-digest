from tts.domain.usecase.generate_article_audio_usecase import GenerateArticleAudioUseCase
from tts.data.text_to_speech_repository_impl import SpeechifyRepository

class TTSContainer:
    def __init__(self):
        self.tts_repository = SpeechifyRepository()
        self.generate_article_audio = GenerateArticleAudioUseCase(
            tts_repository=self.tts_repository
        )


container = TTSContainer()