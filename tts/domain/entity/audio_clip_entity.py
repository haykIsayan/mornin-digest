from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class AudioClip:
    article_id: str
    audio_url: str
    duration_seconds: float
    voice_id: str
    generated_at: datetime