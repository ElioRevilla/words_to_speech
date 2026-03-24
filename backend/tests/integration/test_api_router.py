import shutil
import uuid
from pathlib import Path
from unittest.mock import AsyncMock

from app.application.dto import CombinedAudioResponse, GenerateWordsResponse, WordAudioResponse
from app.infrastructure.main import app, create_app


def test_generate_endpoint_returns_items(monkeypatch):
    use_case = AsyncMock()
    use_case.execute.return_value = GenerateWordsResponse(
        items=[WordAudioResponse(word="resilience", audio_url="/api/audio/x.mp3", audio_filename="x.mp3")]
    )

    app.dependency_overrides.clear()
    from app.infrastructure.container import get_generate_words_batch_use_case

    app.dependency_overrides[get_generate_words_batch_use_case] = lambda: use_case

    from fastapi.testclient import TestClient

    with TestClient(app) as client:
        response = client.post("/api/generate", json={"words": ["resilience"], "slow": False})

    assert response.status_code == 200
    assert response.json()["items"][0]["word"] == "resilience"


def test_combine_audio_endpoint_returns_mix():
    use_case = AsyncMock()
    use_case.execute.return_value = CombinedAudioResponse(
        audio_url="/api/audio/history_mix_123.mp3",
        audio_filename="history_mix_123.mp3",
        item_count=2,
    )

    app.dependency_overrides.clear()
    from app.infrastructure.container import get_combine_history_audio_use_case

    app.dependency_overrides[get_combine_history_audio_use_case] = lambda: use_case

    from fastapi.testclient import TestClient

    with TestClient(app) as client:
        response = client.post("/api/audio/combine", json={"filenames": ["one.mp3", "two.mp3"]})

    assert response.status_code == 200
    assert response.json()["audio_filename"] == "history_mix_123.mp3"
    assert response.json()["item_count"] == 2


def test_health_endpoint():
    from fastapi.testclient import TestClient

    with TestClient(app) as client:
        response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root_serves_frontend_when_dist_exists(monkeypatch):
    dist_path = Path(__file__).resolve().parent / f"_tmp_frontend_dist_{uuid.uuid4().hex}"
    dist_path.mkdir()
    (dist_path / "index.html").write_text("<html>frontend</html>", encoding="utf-8")
    (dist_path / "asset.js").write_text("console.log('ok')", encoding="utf-8")

    monkeypatch.setattr("app.infrastructure.main.get_frontend_dist_path", lambda: dist_path)
    test_app = create_app()

    from fastapi.testclient import TestClient

    try:
        with TestClient(test_app) as client:
            root_response = client.get("/")
            asset_response = client.get("/asset.js")
            spa_response = client.get("/dashboard")
    finally:
        shutil.rmtree(dist_path, ignore_errors=True)

    assert root_response.status_code == 200
    assert "frontend" in root_response.text
    assert asset_response.status_code == 200
    assert "console.log" in asset_response.text
    assert spa_response.status_code == 200
    assert "frontend" in spa_response.text

