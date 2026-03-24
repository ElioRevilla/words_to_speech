from pydantic import BaseModel, Field, model_validator


class GenerateWordsRequest(BaseModel):
    words: list[str] = Field(..., min_length=1, max_length=20, description="One or more English words")
    slow: bool = Field(default=False, description="Generate a slow 0.7x audio variant")

    @model_validator(mode="after")
    def validate_words(self) -> "GenerateWordsRequest":
        cleaned = [word.strip() for word in self.words if word.strip()]
        if not cleaned:
            raise ValueError("At least one non-empty word is required.")
        self.words = cleaned
        return self


class CombineAudioRequest(BaseModel):
    filenames: list[str] = Field(..., min_length=1, max_length=50, description="Existing audio files to combine")

    @model_validator(mode="after")
    def validate_filenames(self) -> "CombineAudioRequest":
        cleaned = [filename.strip() for filename in self.filenames if filename.strip()]
        if not cleaned:
            raise ValueError("At least one audio filename is required.")
        self.filenames = cleaned
        return self


class WordAudioResponse(BaseModel):
    word: str
    phonetic: str | None = None
    spelling: str | None = None
    meaning: str | None = None
    example_en: str | None = None
    example_es: str | None = None
    audio_url: str | None = None
    audio_filename: str | None = None
    slow: bool = False
    error: str | None = None


class GenerateWordsResponse(BaseModel):
    items: list[WordAudioResponse]


class CombinedAudioResponse(BaseModel):
    audio_url: str
    audio_filename: str
    item_count: int
