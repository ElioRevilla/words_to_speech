import hashlib

from app.application.dto import CombinedAudioResponse
from app.application.services.audio_concatenator import AudioConcatenator
from app.domain.ports import AudioStoragePort


class CombineHistoryAudioUseCase:
    def __init__(self, storage: AudioStoragePort, concatenator: AudioConcatenator):
        self._storage = storage
        self._concatenator = concatenator

    async def execute(self, filenames: list[str]) -> CombinedAudioResponse:
        cleaned_filenames: list[str] = []
        seen: set[str] = set()

        for filename in filenames:
            normalized = filename.strip()
            if not normalized or normalized in seen:
                continue
            cleaned_filenames.append(normalized)
            seen.add(normalized)

        file_paths = [await self._storage.get_path(filename) for filename in cleaned_filenames]
        combined_audio = self._concatenator.concatenate_files(file_paths)
        digest = hashlib.sha1("|".join(cleaned_filenames).encode("utf-8")).hexdigest()[:12]
        output_filename = f"history_mix_{digest}.mp3"
        audio_url = await self._storage.save(output_filename, combined_audio)

        return CombinedAudioResponse(
            audio_url=audio_url,
            audio_filename=output_filename,
            item_count=len(cleaned_filenames),
        )
