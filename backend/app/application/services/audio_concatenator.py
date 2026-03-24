from pathlib import Path
import shutil
import subprocess
import tempfile

from app.domain.exceptions import TTSError


class AudioConcatenator:
    def concatenate_bytes(self, parts: list[bytes], silence_ms: int = 500) -> bytes:
        ffmpeg_path = self._get_ffmpeg_path()

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            file_paths: list[Path] = []
            for index, part in enumerate(parts):
                part_path = temp_path / f"part_{index}.mp3"
                part_path.write_bytes(part)
                file_paths.append(part_path)

            return self._concatenate_files(ffmpeg_path, file_paths, temp_path, silence_ms)

    def concatenate_files(self, files: list[str], silence_ms: int = 900) -> bytes:
        ffmpeg_path = self._get_ffmpeg_path()

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            file_paths = [Path(file).resolve() for file in files]
            return self._concatenate_files(ffmpeg_path, file_paths, temp_path, silence_ms)

    def _get_ffmpeg_path(self) -> str:
        ffmpeg_path = shutil.which("ffmpeg")
        if not ffmpeg_path:
            raise TTSError("ffmpeg is required to concatenate audio segments.")
        return ffmpeg_path

    def _concatenate_files(self, ffmpeg_path: str, file_paths: list[Path], temp_path: Path, silence_ms: int) -> bytes:
        concat_entries: list[str] = []

        for index, file_path in enumerate(file_paths):
            concat_entries.append(f"file '{file_path.as_posix()}'")

            if index < len(file_paths) - 1:
                silence_path = temp_path / f"silence_{index}.mp3"
                self._create_silence_segment(ffmpeg_path, silence_path, silence_ms)
                concat_entries.append(f"file '{silence_path.as_posix()}'")

        concat_file = temp_path / "concat.txt"
        concat_file.write_text("\n".join(concat_entries), encoding="utf-8")
        output_path = temp_path / "combined.mp3"

        try:
            subprocess.run(
                [
                    ffmpeg_path,
                    "-y",
                    "-f",
                    "concat",
                    "-safe",
                    "0",
                    "-i",
                    str(concat_file),
                    "-c",
                    "copy",
                    str(output_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as exc:
            raise TTSError(f"ffmpeg concat failed: {exc.stderr.strip()}") from exc

        return output_path.read_bytes()

    def _create_silence_segment(self, ffmpeg_path: str, output_path: Path, silence_ms: int) -> None:
        try:
            subprocess.run(
                [
                    ffmpeg_path,
                    "-y",
                    "-f",
                    "lavfi",
                    "-i",
                    "anullsrc=r=24000:cl=mono",
                    "-t",
                    f"{silence_ms / 1000:.3f}",
                    "-q:a",
                    "9",
                    "-acodec",
                    "libmp3lame",
                    str(output_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as exc:
            raise TTSError(f"ffmpeg silence generation failed: {exc.stderr.strip()}") from exc
