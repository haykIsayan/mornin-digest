from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class AudioClip:
    article_id: str
    audio_data: bytes
    audio_format: str
    voice_id: str
    generated_at: datetime