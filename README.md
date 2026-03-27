# WordSound

A Progressive Web App for Spanish speakers learning English vocabulary. Enter a list of words and WordSound generates pronunciation guides, meanings, example sentences, and educational audio — all powered by Azure AI.

## Features

- Generate pronunciation, meaning, and example sentences for up to 20 English words at once
- Text-to-speech audio in English and Spanish using Azure AI Speech neural voices
- Slow-speed audio variants for pronunciation practice
- Combine multiple word audios into a single study track
- Works offline after first load (PWA with service worker caching)
- Installable on desktop and mobile

## Tech Stack

**Backend**
- Python 3.12 + FastAPI
- Azure OpenAI (GPT-4o mini) for content generation
- Azure AI Speech REST API for text-to-speech
- ffmpeg for audio concatenation
- Clean Architecture (domain, application, adapters, infrastructure)

**Frontend**
- React 18 + Vite
- Tailwind CSS
- PWA with offline support via vite-plugin-pwa

**Infrastructure**
- Docker (multi-stage build — frontend + backend in a single image)
- Azure Container Registry
- Azure App Service (Linux container)
- GitHub Actions CI/CD with OIDC authentication (no stored credentials)

## Architecture

```
frontend/          React PWA (built into backend's static files)
backend/
  app/
    domain/        Entities, ports, exceptions (no external dependencies)
    application/   Use cases and DTOs
    adapters/      Inbound (HTTP routers) and outbound (Azure services)
    infrastructure/  FastAPI app, settings, dependency injection
```

## Local Setup

### Requirements

- Python 3.12+
- Node.js 20+
- ffmpeg installed on your system
- Azure OpenAI deployment (GPT-4o mini recommended)
- Azure AI Speech resource

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate       # Windows
source .venv/bin/activate    # macOS/Linux
pip install -r requirements.txt
copy .env.example .env       # then fill in your values
uvicorn app.infrastructure.main:app --reload
```

Required variables in `backend/.env`:

| Variable | Description |
|----------|-------------|
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL |
| `AZURE_OPENAI_DEPLOYMENT` | Deployment name (e.g. `gpt-4o-mini`) |
| `AZURE_OPENAI_API_VERSION` | API version (e.g. `2024-10-21`) |
| `AZURE_SPEECH_KEY` | Azure AI Speech key |
| `AZURE_SPEECH_REGION` | Azure region (e.g. `eastus`) |

Optional:

| Variable | Default | Description |
|----------|---------|-------------|
| `AZURE_SPEECH_VOICE_EN` | `en-US-AvaMultilingualNeural` | English TTS voice |
| `AZURE_SPEECH_VOICE_ES` | `es-US-AlonsoNeural` | Spanish TTS voice |
| `AUDIO_STORAGE_PATH` | `./tmp/wordsound_audio` | Local audio file storage |
| `ALLOWED_ORIGINS` | `["http://localhost:5173"]` | CORS allowed origins |
| `API_AUDIO_BASE_URL` | `/api/audio` | Public base URL for audio files |

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend expects the backend running at `http://localhost:8000` by default.

## Docker

```bash
docker compose up --build
```

This starts both backend (port 8000) and frontend (port 5173) with hot reload.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/generate` | Generate word entries with audio |
| `GET` | `/api/audio/{filename}` | Stream an audio file |
| `POST` | `/api/audio/combine` | Combine multiple audio files |
| `GET` | `/api/health` | Health check |

### POST /api/generate

```json
{
  "words": ["ephemeral", "resilient"],
  "slow": false
}
```

Returns an array of word entries with pronunciation, meaning, examples, and audio URLs.

## Deployment

The project uses GitHub Actions to build and push a Docker image to Azure Container Registry, then deploy to Azure App Service.

Required GitHub secrets: `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`, `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_DEPLOYMENT`, `AZURE_SPEECH_KEY`, `AZURE_SPEECH_REGION`.

Authentication uses **OIDC Federated Identity** — no passwords stored in GitHub.
