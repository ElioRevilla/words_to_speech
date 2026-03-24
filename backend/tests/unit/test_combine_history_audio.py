from unittest.mock import AsyncMock, Mock

import pytest

from app.application.use_cases.combine_history_audio import CombineHistoryAudioUseCase


@pytest.mark.asyncio
async def test_combine_history_audio_creates_stable_filename() -> None:
    mock_storage = AsyncMock()
    mock_storage.get_path.side_effect = ["C:/audio/one.mp3", "C:/audio/two.mp3"]
    mock_storage.save.return_value = "/api/audio/history_mix_abcd1234.mp3"

    mock_concatenator = Mock()
    mock_concatenator.concatenate_files.return_value = b"combined_audio"

    use_case = CombineHistoryAudioUseCase(storage=mock_storage, concatenator=mock_concatenator)

    result = await use_case.execute(["one.mp3", "two.mp3", "one.mp3"])

    assert result.audio_url == "/api/audio/history_mix_abcd1234.mp3"
    assert result.audio_filename.startswith("history_mix_")
    assert result.item_count == 2
    mock_concatenator.concatenate_files.assert_called_once_with(["C:/audio/one.mp3", "C:/audio/two.mp3"])
