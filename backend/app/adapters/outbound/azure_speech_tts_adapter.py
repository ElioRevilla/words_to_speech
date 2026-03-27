from xml.sax.saxutils import escape

import httpx

from app.domain.exceptions import TTSError
from app.domain.ports import TTSPort


class AzureSpeechTTSAdapter(TTSPort):
    def __init__(
        self,
        speech_key: str,
        speech_region: str,
        english_voice: str = "en-US-AvaMultilingualNeural",
        spanish_voice: str = "es-US-AlonsoNeural",
    ):
        self._speech_key = speech_key
        self._speech_region = speech_region
        self._english_voice = english_voice
        self._spanish_voice = spanish_voice

    async def synthesize_speech(
        self,
        text: str,
        language_code: str,
        speaking_rate: float = 1.0,
    ) -> bytes:
        url = f"https://{self._speech_region}.tts.speech.microsoft.com/cognitiveservices/v1"
        headers = {
            "Ocp-Apim-Subscription-Key": self._speech_key,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-24khz-48kbitrate-mono-mp3",
            "User-Agent": "wordsound",
        }
        ssml = self._build_ssml(text, language_code, speaking_rate)

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, content=ssml.encode("utf-8"), headers=headers)

            if response.status_code == 200:
                return response.content

            raise TTSError(
                f"Azure Speech REST API returned {response.status_code}: {response.text}"
            )
        except TTSError:
            raise
        except Exception as exc:
            raise TTSError(f"TTS synthesis failed: {exc}") from exc

    def _build_ssml(self, text: str, language_code: str, speaking_rate: float) -> str:
        voice_name = self._english_voice if language_code.startswith("en") else self._spanish_voice
        rate_percent = int(round((speaking_rate - 1.0) * 100))
        rate_value = f"{rate_percent:+d}%"
        escaped_text = escape(text)

        return f"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{language_code}">
  <voice name="{voice_name}">
    <prosody rate="{rate_value}">{escaped_text}</prosody>
  </voice>
</speak>""".strip()
