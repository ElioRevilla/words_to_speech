import uuid

from app.application.dto import WordAudioResponse
from app.application.services.audio_concatenator import AudioConcatenator
from app.domain.entities import AudioSegment
from app.domain.ports import AudioStoragePort, LLMPort, TTSPort


class GenerateWordAudioUseCase:
    def __init__(self, llm: LLMPort, tts: TTSPort, storage: AudioStoragePort, concatenator: AudioConcatenator):
        self._llm = llm
        self._tts = tts
        self._storage = storage
        self._concatenator = concatenator

    async def execute(self, word: str, slow: bool = False) -> WordAudioResponse:
        word_entry = await self._llm.generate_word_content(word)
        segments = self._build_segments(word_entry, slow)

        audio_parts: list[bytes] = []
        for segment in segments:
            audio_parts.append(
                await self._tts.synthesize_speech(
                    text=segment.text,
                    language_code=segment.language_code,
                    speaking_rate=segment.speaking_rate,
                )
            )

        combined = self._concatenator.concatenate_bytes(audio_parts)
        suffix = "slow" if slow else "normal"
        filename = f"{word_entry.word}_{suffix}_{uuid.uuid4().hex[:8]}.mp3"
        audio_url = await self._storage.save(filename, combined)
        return WordAudioResponse(
            word=word_entry.word,
            phonetic=word_entry.phonetic,
            spelling=word_entry.spelling,
            meaning=word_entry.meaning,
            example_en=word_entry.example_en,
            example_es=word_entry.example_es,
            audio_url=audio_url,
            audio_filename=filename,
            slow=slow,
        )

    def _build_segments(self, word_entry, slow: bool) -> list[AudioSegment]:
        if slow:
            rate = 0.7
            return [
                AudioSegment(f"The word is: {word_entry.word}", "en-US", rate),
                AudioSegment(f"It is spelled: {word_entry.spelling.replace('-', ', ')}", "en-US", rate),
                AudioSegment(f"It means: {word_entry.meaning}", "en-US", rate),
                AudioSegment(f"For example: {word_entry.example_en}", "en-US", rate),
                AudioSegment(f"En espanol: {word_entry.example_es}", "es-US", rate),
            ]

        return [
            AudioSegment(f"The word is: {word_entry.word}", "en-US", 0.9),
            AudioSegment(f"It is spelled: {word_entry.spelling.replace('-', ', ')}", "en-US", 0.85),
            AudioSegment(f"It means: {word_entry.meaning}", "en-US", 0.95),
            AudioSegment(f"For example: {word_entry.example_en}", "en-US", 0.95),
            AudioSegment(f"En espanol: {word_entry.example_es}", "es-US", 0.95),
        ]
