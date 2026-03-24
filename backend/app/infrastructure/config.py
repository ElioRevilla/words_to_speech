from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    azure_openai_api_key: str = Field(default="test-key", alias="AZURE_OPENAI_API_KEY")
    azure_openai_endpoint: str = Field(
        default="https://example-resource.openai.azure.com",
        alias="AZURE_OPENAI_ENDPOINT",
    )
    azure_openai_deployment: str = Field(default="gpt-4o-mini", alias="AZURE_OPENAI_DEPLOYMENT")
    azure_openai_api_version: str = Field(default="2024-10-21", alias="AZURE_OPENAI_API_VERSION")
    azure_speech_key: str = Field(default="test-key", alias="AZURE_SPEECH_KEY")
    azure_speech_region: str = Field(default="eastus", alias="AZURE_SPEECH_REGION")
    azure_speech_voice_en: str = Field(
        default="en-US-AvaMultilingualNeural",
        alias="AZURE_SPEECH_VOICE_EN",
    )
    azure_speech_voice_es: str = Field(
        default="es-US-AlonsoNeural",
        alias="AZURE_SPEECH_VOICE_ES",
    )
    audio_storage_path: str = Field(default="./tmp/wordsound_audio", alias="AUDIO_STORAGE_PATH")
    allowed_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:5173"],
        alias="ALLOWED_ORIGINS",
    )
    api_audio_base_url: str = Field(
        default="/api/audio",
        alias="API_AUDIO_BASE_URL",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
        extra="ignore",
    )
