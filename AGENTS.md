# Repository Guidelines

## Project Structure & Module Organization
This repository is split into two apps:

- `backend/`: FastAPI service organized with Clean Architecture. Core domain code lives in `app/domain`, application use cases in `app/application`, HTTP routers in `app/adapters/inbound`, external integrations in `app/adapters/outbound`, and startup/config in `app/infrastructure`.
- `backend/tests/unit` and `backend/tests/integration`: backend test suites.
- `frontend/`: Vite + React PWA. UI components live in `src/components`, hooks in `src/hooks`, API calls in `src/services`, and shared styles in `src/styles`.
- `docker-compose.yml`: local full-stack orchestration.

## Build, Test, and Development Commands
- `cd backend && python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt`: create and install the backend environment.
- `cd backend && uvicorn app.infrastructure.main:app --reload`: run the API locally on port `8000`.
- `cd backend && pytest`: run unit and integration tests.
- `cd frontend && npm install`: install the frontend dependencies.
- `cd frontend && npm run dev`: start the Vite dev server on port `5173`.
- `cd frontend && npm run build`: produce a production build.
- `docker compose up --build`: run frontend and backend together.

## Coding Style & Naming Conventions
Follow the style already present in the codebase:

- Python: 4-space indentation, type hints, `snake_case` for functions/modules, `PascalCase` for classes.
- React: components in `PascalCase` files such as `WordCard.jsx`, hooks prefixed with `use`, service modules in `camelCase`/lowercase such as `api.js`.
- Keep domain logic in `backend/app/domain` and avoid leaking framework code into it.
- No formatter or linter config is committed yet; keep changes small and consistent with nearby code.

## Testing Guidelines
Backend tests use `pytest` with `pytest-asyncio`. Add unit tests under `backend/tests/unit` and API-level tests under `backend/tests/integration`. Name files `test_<feature>.py` and keep fixtures in `backend/tests/conftest.py`. Run `pytest` before opening a PR.

## Security & Configuration Tips
Backend settings are loaded from `backend/.env` via `backend/.env.example`. Keep secrets out of source control. `ffmpeg` is required for MP3 concatenation, and audio files are written under the configured `AUDIO_STORAGE_PATH`.

## Commit & Pull Request Guidelines
This workspace does not include `.git` history, so no repository-specific commit pattern could be verified. Use short, imperative commit subjects such as `Add batch word generation test`. PRs should include a clear summary, testing notes, linked issues, and screenshots or sample API payloads when UI or contract behavior changes.
