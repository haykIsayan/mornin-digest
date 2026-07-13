from abc import ABC, abstractmethod
from tts.domain.entity.audio_clip_entity import AudioClip


class TextToSpeechRepository(ABC):
    @abstractmethod
    async def synthesize(self, text: str, voice_id: str) -> AudioClip:
        """Convert text to speech and return metadata about the generated clip."""
        raise NotImplementedError