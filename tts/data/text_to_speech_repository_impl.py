from datetime import datetime, timezone
import base64
from speechify import AsyncSpeechify
from tts.domain.entity.audio_clip_entity import AudioClip
from tts.domain.repository.text_to_speech_repository import TextToSpeechRepository


class SpeechifyRepository(TextToSpeechRepository):
    def __init__(self, audio_format: str = "mp3", model: str = "simba-english"):
        self._client = AsyncSpeechify()  # reads SPEECHIFY_API_KEY from env
        self._audio_format = audio_format
        self._model = model

    async def synthesize(self, article_id: str, text: str, voice_id: str) -> AudioClip:
        response = await self._client.tts.audio.speech(
            input=text,
            voice_id=voice_id,
            audio_format=self._audio_format,
            model=self._model,
        )

        audio_bytes = base64.b64decode(response.audio_data)

        return AudioClip(
            article_id=article_id,
            audio_data=audio_bytes,
            audio_format=self._audio_format,
            voice_id=voice_id,
            generated_at=datetime.now(timezone.utc),
        )