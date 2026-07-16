from tts.domain.entity.audio_clip_entity import AudioClip
from tts.domain.repository.text_to_speech_repository import TextToSpeechRepository


class GenerateArticleAudioUseCase:
    def __init__(self, tts_repository: TextToSpeechRepository):
        self._tts_repository = tts_repository

    async def execute(self, article_id: str, text: str, voice_id: str) -> AudioClip:
        return await self._tts_repository.synthesize(article_id=article_id, text=text, voice_id=voice_id)