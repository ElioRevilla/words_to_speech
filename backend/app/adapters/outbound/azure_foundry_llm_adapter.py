import json

from openai import AsyncAzureOpenAI

from app.domain.entities import WordEntry
from app.domain.exceptions import LLMError
from app.domain.ports import LLMPort

SYSTEM_PROMPT = """You are a bilingual English-Spanish language assistant.
Given an English word, return JSON with these keys:
phonetic, spelling, meaning, example_en, example_es.
Rules:
- meaning must be concise and in English
- example_en must sound natural
- example_es must be a faithful Spanish translation
- spelling must use uppercase letters separated by hyphens
Respond with JSON only."""


class AzureFoundryLLMAdapter(LLMPort):
    def __init__(
        self,
        api_key: str,
        endpoint: str,
        deployment: str,
        api_version: str = "2024-10-21",
    ):
        self._client = AsyncAzureOpenAI(
            api_key=api_key,
            azure_endpoint=endpoint.rstrip("/"),
            api_version=api_version,
        )
        self._deployment = deployment

    async def generate_word_content(self, word: str) -> WordEntry:
        try:
            response = await self._client.chat.completions.create(
                model=self._deployment,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": word},
                ],
                temperature=0.3,
                max_tokens=300,
            )
            raw_content = response.choices[0].message.content or "{}"
            data = json.loads(raw_content)
            required_keys = {"phonetic", "spelling", "meaning", "example_en", "example_es"}
            missing_keys = sorted(required_keys - set(data))
            if missing_keys:
                raise LLMError(f"Missing keys from model response: {', '.join(missing_keys)}")

            return WordEntry(
                word=word,
                phonetic=data["phonetic"].strip(),
                spelling=data["spelling"].strip(),
                meaning=data["meaning"].strip(),
                example_en=data["example_en"].strip(),
                example_es=data["example_es"].strip(),
            )
        except LLMError:
            raise
        except Exception as exc:
            raise LLMError(f"Failed to generate content for '{word}': {exc}") from exc
