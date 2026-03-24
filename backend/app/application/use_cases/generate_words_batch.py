from app.application.dto import GenerateWordsRequest, GenerateWordsResponse, WordAudioResponse
from app.application.use_cases.generate_word_audio import GenerateWordAudioUseCase
from app.domain.exceptions import DomainError


class GenerateWordsBatchUseCase:
    def __init__(self, generate_word_audio: GenerateWordAudioUseCase):
        self._generate_word_audio = generate_word_audio

    async def execute(self, request: GenerateWordsRequest) -> GenerateWordsResponse:
        items: list[WordAudioResponse] = []
        for word in request.words:
            try:
                items.append(await self._generate_word_audio.execute(word=word, slow=request.slow))
            except DomainError as exc:
                items.append(WordAudioResponse(word=word, slow=request.slow, error=str(exc)))

        return GenerateWordsResponse(items=items)
