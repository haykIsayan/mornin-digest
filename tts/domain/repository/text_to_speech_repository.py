from abc import ABC, abstractmethod
from tts.domain.entity.audio_clip_entity import AudioClip


class TextToSpeechRepository(ABC):
    @abstractmethod
    async def synthesize(self, article_id: str, text: str, voice_id: str) -> AudioClip:
        pass