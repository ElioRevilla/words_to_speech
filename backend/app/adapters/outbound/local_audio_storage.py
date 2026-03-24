from pathlib import Path

from app.domain.ports import AudioStoragePort


class LocalAudioStorage(AudioStoragePort):
    def __init__(self, base_path: str, public_base_url: str):
        self._base_path = Path(base_path).resolve()
        self._public_base_url = public_base_url.rstrip("/")
        self._base_path.mkdir(parents=True, exist_ok=True)

    async def save(self, filename: str, audio_data: bytes) -> str:
        target = self._base_path / filename
        target.write_bytes(audio_data)
        return f"{self._public_base_url}/{filename}"

    async def get_path(self, filename: str) -> str:
        target = (self._base_path / filename).resolve()
        try:
            target.relative_to(self._base_path)
        except ValueError as exc:
            raise FileNotFoundError(filename) from exc
        if not target.exists():
            raise FileNotFoundError(filename)
        return str(target)

