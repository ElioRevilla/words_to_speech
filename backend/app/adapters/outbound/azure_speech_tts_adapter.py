import asyncio
from xml.sax.saxutils import escape

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
        try:
            return await asyncio.to_thread(
                self._synthesize,
                text,
                language_code,
                speaking_rate,
            )
        except TTSError:
            raise
        except Exception as exc:
            raise TTSError(f"TTS synthesis failed: {exc}") from exc

    def _synthesize(self, text: str, language_code: str, speaking_rate: float) -> bytes:
        speechsdk = self._load_speechsdk()
        speech_config = speechsdk.SpeechConfig(
            subscription=self._speech_key,
            region=self._speech_region,
        )
        speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Audio24Khz48KBitRateMonoMp3
        )

        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=None,
        )
        result = synthesizer.speak_ssml_async(
            self._build_ssml(text, language_code, speaking_rate)
        ).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return result.audio_data

        details = speechsdk.SpeechSynthesisCancellationDetails.from_result(result)
        reason = getattr(details.reason, "name", str(details.reason))
        error_details = details.error_details or "unknown error"
        raise TTSError(f"Azure Speech synthesis failed ({reason}): {error_details}")

    def _load_speechsdk(self):
        try:
            import azure.cognitiveservices.speech as speechsdk
        except ImportError as exc:
            raise TTSError(
                "azure-cognitiveservices-speech is not installed. Run 'pip install -r requirements.txt'."
            ) from exc
        return speechsdk

    def _build_ssml(self, text: str, language_code: str, speaking_rate: float) -> str:
        voice_name = self._english_voice if language_code.startswith("en") else self._spanish_voice
        rate_percent = int(round((speaking_rate - 1.0) * 100))
        rate_value = f"{rate_percent:+d}%"
        escaped_text = escape(text)

        return f"""
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{language_code}">
  <voice name="{voice_name}">
    <prosody rate="{rate_value}">{escaped_text}</prosody>
  </voice>
</speak>
""".strip()
