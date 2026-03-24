from abc import ABC, abstractmethod

from app.domain.entities import WordEntry


class LLMPort(ABC):
    @abstractmethod
    async def generate_word_content(self, word: str) -> WordEntry:
        ...


class TTSPort(ABC):
    @abstractmethod
    async def synthesize_speech(self, text: str, language_code: str, speaking_rate: float = 1.0) -> bytes:
        ...


class AudioStoragePort(ABC):
    @abstractmethod
    async def save(self, filename: str, audio_data: bytes) -> str:
        ...

    @abstractmethod
    async def get_path(self, filename: str) -> str:
        ...
