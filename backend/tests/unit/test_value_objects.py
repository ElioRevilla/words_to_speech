import pytest

from app.domain.exceptions import DomainError
from app.domain.value_objects import ExampleSentence, Phonetic, Spelling


def test_phonetic_rejects_empty() -> None:
    with pytest.raises(DomainError):
        Phonetic("")


def test_spelling_accepts_hyphenated_letters() -> None:
    spelling = Spelling("R-E-S-I-L-I-E-N-C-E")
    assert spelling.value.endswith("E")


def test_example_sentence_requires_both_languages() -> None:
    with pytest.raises(DomainError):
        ExampleSentence("Hello", "")
