from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.domain.entities import WordEntry
from app.infrastructure.main import app


@pytest.fixture
def sample_word_entry() -> WordEntry:
    return WordEntry(
        word="resilience",
        phonetic="/rɪzɪl.i.əns/",
        spelling="R-E-S-I-L-I-E-N-C-E",
        meaning="The ability to recover quickly from difficulties.",
        example_en="Her resilience helped her overcome challenges.",
        example_es="Su resiliencia la ayudó a superar desafíos.",
    )


@pytest.fixture
def mock_generate_use_case():
    return AsyncMock()


@pytest.fixture
def client():
    return TestClient(app)
