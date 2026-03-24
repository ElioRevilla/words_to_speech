from unittest.mock import AsyncMock, Mock

import pytest

from app.application.use_cases.generate_word_audio import GenerateWordAudioUseCase


@pytest.mark.asyncio
async def test_generate_word_audio_success(sample_word_entry) -> None:
    mock_llm = AsyncMock()
    mock_llm.generate_word_content.return_value = sample_word_entry

    mock_tts = AsyncMock()
    mock_tts.synthesize_speech.return_value = b"fake_audio_bytes"

    mock_storage = AsyncMock()
    mock_storage.save.return_value = "/api/audio/resilience_normal_abc123.mp3"

    mock_concatenator = Mock()
    mock_concatenator.concatenate_bytes.return_value = b"combined_audio"

    use_case = GenerateWordAudioUseCase(
        llm=mock_llm,
        tts=mock_tts,
        storage=mock_storage,
        concatenator=mock_concatenator,
    )

    result = await use_case.execute("resilience")

    assert result.word == "resilience"
    assert result.audio_url == "/api/audio/resilience_normal_abc123.mp3"
    assert mock_tts.synthesize_speech.call_count == 5
    mock_concatenator.concatenate_bytes.assert_called_once()


@pytest.mark.asyncio
async def test_generate_word_audio_slow_uses_seven_tenths_rate(sample_word_entry) -> None:
    mock_llm = AsyncMock()
    mock_llm.generate_word_content.return_value = sample_word_entry

    mock_tts = AsyncMock()
    mock_tts.synthesize_speech.return_value = b"fake_audio_bytes"

    mock_storage = AsyncMock()
    mock_storage.save.return_value = "/api/audio/resilience_slow_abc123.mp3"

    mock_concatenator = Mock()
    mock_concatenator.concatenate_bytes.return_value = b"combined_audio"

    use_case = GenerateWordAudioUseCase(
        llm=mock_llm,
        tts=mock_tts,
        storage=mock_storage,
        concatenator=mock_concatenator,
    )

    result = await use_case.execute("resilience", slow=True)

    assert result.slow is True
    rates = [call.kwargs["speaking_rate"] for call in mock_tts.synthesize_speech.await_args_list]
    assert rates == [0.7, 0.7, 0.7, 0.7, 0.7]
