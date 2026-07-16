
from fastapi import Form, Depends
from fastapi import APIRouter
from fastapi.responses import Response
from pydantic import BaseModel
from auth.api.auth_middleware import get_current_user
from tts.tts_container import container as tts_container

router = APIRouter(prefix="/tts", tags=["tts"])

class SynthesizeRequest(BaseModel):
    text: str
    voice_id: str = "george"


@router.post("/synthesize/{article_id}")
async def synthesize_article_audio(
    article_id: str,
    request: SynthesizeRequest,
    user_id: str =  Depends(get_current_user)
):
    clip = await tts_container.generate_article_audio.execute(
        article_id=article_id,
        text=request.text,
        voice_id=request.voice_id,
    )

    return Response(
        content=clip.audio_data,
        media_type="audio/mpeg",
        headers={
            "Content-Disposition": f'inline; filename="{article_id}.mp3"',
        },
    )