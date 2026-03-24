# WordSound

PWA para practicar vocabulario en ingles con audio educativo generado por un backend FastAPI.
La generacion de contenido usa un deployment de Azure AI Foundry / Azure OpenAI y la sintesis de audio usa Azure AI Speech.

## Local

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.infrastructure.main:app --reload
```

Variables necesarias en `backend/.env`:

- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_DEPLOYMENT`
- `AZURE_OPENAI_API_VERSION`
- `AZURE_SPEECH_KEY`
- `AZURE_SPEECH_REGION`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Docker

```bash
docker compose up --build
```

## Notas

- El backend expone `POST /api/generate`, `GET /api/audio/{filename}` y `GET /api/health`.
- `ffmpeg` es requerido para concatenar MP3 dentro del contenedor backend.
- Las voces de Azure Speech se pueden ajustar con `AZURE_SPEECH_VOICE_EN` y `AZURE_SPEECH_VOICE_ES`.
