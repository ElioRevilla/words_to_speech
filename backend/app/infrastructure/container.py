from functools import lru_cache

from app.adapters.outbound.azure_foundry_llm_adapter import AzureFoundryLLMAdapter
from app.adapters.outbound.azure_speech_tts_adapter import AzureSpeechTTSAdapter
from app.adapters.outbound.local_audio_storage import LocalAudioStorage
from app.application.services.audio_concatenator import AudioConcatenator
from app.application.use_cases.combine_history_audio import CombineHistoryAudioUseCase
from app.application.use_cases.generate_word_audio import GenerateWordAudioUseCase
from app.application.use_cases.generate_words_batch import GenerateWordsBatchUseCase
from app.infrastructure.config import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_audio_storage() -> LocalAudioStorage:
    settings = get_settings()
    return LocalAudioStorage(
        base_path=settings.audio_storage_path,
        public_base_url=settings.api_audio_base_url,
    )


@lru_cache
def get_audio_concatenator() -> AudioConcatenator:
    return AudioConcatenator()


@lru_cache
def get_generate_word_audio_use_case() -> GenerateWordAudioUseCase:
    settings = get_settings()
    return GenerateWordAudioUseCase(
        llm=AzureFoundryLLMAdapter(
            api_key=settings.azure_openai_api_key,
            endpoint=settings.azure_openai_endpoint,
            deployment=settings.azure_openai_deployment,
            api_version=settings.azure_openai_api_version,
        ),
        tts=AzureSpeechTTSAdapter(
            speech_key=settings.azure_speech_key,
            speech_region=settings.azure_speech_region,
            english_voice=settings.azure_speech_voice_en,
            spanish_voice=settings.azure_speech_voice_es,
        ),
        storage=get_audio_storage(),
        concatenator=get_audio_concatenator(),
    )


@lru_cache
def get_combine_history_audio_use_case() -> CombineHistoryAudioUseCase:
    return CombineHistoryAudioUseCase(
        storage=get_audio_storage(),
        concatenator=get_audio_concatenator(),
    )


def get_generate_words_batch_use_case() -> GenerateWordsBatchUseCase:
    return GenerateWordsBatchUseCase(generate_word_audio=get_generate_word_audio_use_case())
