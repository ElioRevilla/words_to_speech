from dataclasses import dataclass

from app.domain.exceptions import DomainError


@dataclass(frozen=True)
class Phonetic:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise DomainError("Phonetic transcription cannot be empty.")


@dataclass(frozen=True)
class Spelling:
    value: str

    def __post_init__(self) -> None:
        cleaned = self.value.replace("-", "").strip()
        if not cleaned.isalpha():
            raise DomainError("Spelling must contain only letters separated by hyphens.")


@dataclass(frozen=True)
class ExampleSentence:
    english: str
    spanish: str

    def __post_init__(self) -> None:
        if not self.english.strip() or not self.spanish.strip():
            raise DomainError("Example sentences cannot be empty.")
