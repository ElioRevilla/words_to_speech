from dataclasses import dataclass


@dataclass(frozen=True)
class WordEntry:
    word: str
    phonetic: str
    spelling: str
    meaning: str
    example_en: str
    example_es: str


@dataclass(frozen=True)
class AudioSegment:
    text: str
    language_code: str
    speaking_rate: float = 0.95


@dataclass(frozen=True)
class AudioResult:
    word_entry: WordEntry
    audio_url: str
    audio_filename: str
    slow: bool = False
