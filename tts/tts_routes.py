from fastapi import APIRouter

from tts.tts_container import container as tts_container

router = APIRouter(tags=["tts"])
