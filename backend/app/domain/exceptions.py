class DomainError(Exception):
    """Base domain exception."""


class LLMError(DomainError):
    """Raised when the language model provider fails."""


class TTSError(DomainError):
    """Raised when the text-to-speech provider fails."""


class WordNotFoundError(DomainError):
    """Raised when a word cannot be resolved."""
