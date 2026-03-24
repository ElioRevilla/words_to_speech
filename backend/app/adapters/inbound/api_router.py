from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from app.application.dto import CombineAudioRequest, CombinedAudioResponse, GenerateWordsRequest, GenerateWordsResponse
from app.application.use_cases.combine_history_audio import CombineHistoryAudioUseCase
from app.application.use_cases.generate_words_batch import GenerateWordsBatchUseCase
from app.infrastructure.container import (
    get_audio_storage,
    get_combine_history_audio_use_case,
    get_generate_words_batch_use_case,
)

router = APIRouter(prefix="/api", tags=["words"])


@router.post("/generate", response_model=GenerateWordsResponse)
async def generate_words(
    request: GenerateWordsRequest,
    use_case: GenerateWordsBatchUseCase = Depends(get_generate_words_batch_use_case),
) -> GenerateWordsResponse:
    return await use_case.execute(request)


@router.post("/audio/combine", response_model=CombinedAudioResponse)
async def combine_audio(
    request: CombineAudioRequest,
    use_case: CombineHistoryAudioUseCase = Depends(get_combine_history_audio_use_case),
) -> CombinedAudioResponse:
    return await use_case.execute(request.filenames)


@router.get("/audio/{filename}")
async def get_audio(filename: str):
    storage = get_audio_storage()
    try:
        path = await storage.get_path(filename)
        return FileResponse(path, media_type="audio/mpeg", filename=filename)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Audio not found") from exc
