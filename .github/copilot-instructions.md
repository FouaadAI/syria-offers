# Copilot Instructions — Syria Offers (Offria)

## Repository Layout

Monorepo with two main parts:

- **`backend/`** — FastAPI Python backend (PostgreSQL, Redis, Alembic, Pydantic v2)
- **`syria_offers_app/`** — Flutter frontend (Android/iOS)

Root-level backend tests live in `tests/`.

---

## Build, Test, and Lint Commands

### Backend (`backend/`)

```bash
# Install dependencies
pip install -r requirements.txt

# Run server (dev)
cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run a single test file (from repo root)
pytest tests/test_auth_api.py -v

# Run all backend tests
pytest tests/ -v

# Database migrations (from backend/)
cd backend && alembic upgrade head
```

### Frontend (`syria_offers_app/`)

```bash
# Analyze
cd syria_offers_app && flutter analyze

# Build APK
cd syria_offers_app && flutter build apk

# Run a single test
cd syria_offers_app && flutter test test/widget/some_test.dart

# Run all tests
cd syria_offers_app && flutter test
```

### Quality Gate (Flutter — Required Before Commit)

Run from `syria_offers_app/`:

```bash
dart format lib test \
  && dart fix lib --apply --code=unused_import,duplicate_import,prefer_single_quotes \
  && dart fix test --apply --code=unused_import,duplicate_import,prefer_single_quotes
```

### Docker Services (Postgres + Redis)

```bash
docker-compose -f backend/docker-compose.yml up -d
```

---

## High-Level Architecture

### Backend (FastAPI)

- **Entry point:** `backend/app/main.py`
- **Routers:** Modular API v1 routers under `backend/app/api/v1/` — auth, offers, bookings, categories, payments, uploads, merchant, admin, chatbot, recommendations, flash_deals, travel_planner, reports
- **Database:** PostgreSQL + SQLAlchemy 2.x ORM. Alembic migrations in `backend/alembic/`.
- **Caching/Rate Limiting:** Redis + SlowAPI (`100/minute` default).
- **Auth:** JWT with `python-jose`, bcrypt passwords, email verification via Brevo SMTP.
- **AI:** Gemini API (`google-genai`) for chatbot and travel planner with function calling (`search_offers`, `plan_trip`).
- **Image validation:** Custom `backend/app/services/image_validation.py` (Gemini Vision + python-magic + Pillow/EXIF stripping).
- **Config:** `backend/app/core/config.py` reads from `.env`. Do **not** hardcode secrets.

### Frontend (Flutter)

> ⚠️ **Critical divergence:** The codebase has extensive `.github/skills/` and `AGENTS.md` defining a `lib/src/` + BLoC + GetX + Dio architecture. The **actual code does not follow this**. Copilot must match the existing code, not the aspirational skills.

- **Actual state:** Flat `lib/` structure (`lib/models/`, `lib/screens/`, `lib/services/`, `lib/widgets/`)
- **State management:** `Provider` (not BLoC/GetX)
- **HTTP client:** `package:http` (not Dio)
- **Navigation:** `MaterialApp` with named `routes` and `Navigator.push` (not GetX / GoRouter)
- **Localization:** Custom `AppLocalizations` class in `lib/localization/` with `AppLocalizationsDelegate` (not GetX `.tr`)
- **Dependency injection:** `MultiProvider` at app root in `main.dart` (not GetX `lazyPut` / injectable)
- **Design system:** ThemeData in `main.dart` with hardcoded colors; no formal design tokens file yet

When editing Flutter code, follow the **existing flat structure** and **Provider + http patterns**. Do not introduce BLoC, GetX, Dio, or `lib/src/` reorganization unless explicitly asked.

### Integration Points

- Flutter `lib/config.dart` sets `baseUrl` to the backend API.
- Backend CORS is open (`allow_origins=["*"]`) — do not assume production hardening is present.
- Guest user (`phone="0000000000"`) is auto-created on startup for anonymous flows.

---

## Key Conventions

### Backend

- **Models:** SQLAlchemy declarative models in `backend/app/models/`. Import models in `main.py` to ensure `Base.metadata` registration.
- **Schemas:** Pydantic v2 schemas in `backend/app/schemas/`.
- **Services:** Business logic lives in `backend/app/services/` (e.g., `payment.py`, `recommender.py`, `travel_planner.py`).
- **Tests:** pytest with SQLite in-memory (`tests/test_api.db`) via `conftest.py`. ARRAY type compiled to TEXT for SQLite compatibility.
- **Secrets:** Must come from `.env`. Never commit API keys, SMTP passwords, or `SECRET_KEY`.

### Frontend

- **Imports:** `analysis_options.yaml` enforces `always_use_package_imports: true`. Use `package:syria_offers_app/...` imports, not relative `../../...` paths.
- **Strings:** All user-facing text must go through `AppLocalizations`. Do not hardcode Arabic/English strings in widgets.
- **Lint rules:** `prefer_single_quotes`, `avoid_print`, `require_trailing_commas`, `prefer_const_constructors` are enforced.
- **Assets:** Only `assets/logo.png` and `.env` are declared in `pubspec.yaml`. Add new assets there if needed.
- **Screens:** State is often kept in `StatefulWidget` screens with direct service calls. Keep changes consistent with this pattern.

### Pull Requests

- PR template gate (`.github/workflows/pr-template-gate.yml`) enforces:
  - Required sections: Issue Explanation, Checklist, Notes for Code Reviewer, Screenshots, Paired with
  - Checklist items must be checked `[x]`
  - Screenshots required unless explicitly stating `No UI`
  - Reviewer notes must contain actual content (not just the example text)

### Commit / Push / PR Gate

After completing any UI or API feature, ask the user in strict order:

1. `Do you want me to commit now? (yes/no)`
2. `Do you want me to push now? (yes/no)`
3. `Do you want me to create PR now? (yes/no)`

Execute only the steps confirmed with `yes`. Stop and report status on `no`.

---

## Flutter-Specific Skills and Rules

For work inside `syria_offers_app/`, also consult the local instruction packs:

- **Existing copilot instructions:** `syria_offers_app/.github/copilot-instructions.md`
- **Skills:** `syria_offers_app/.github/skills/<skill>/SKILL.md`
- **Rules:** `syria_offers_app/.github/rules/*.md`
- **AGENTS.md:** `syria_offers_app/AGENTS.md` (mirrors skills/rules with `.codex` paths)

When a task maps to a skill description, read the matching `SKILL.md` before writing code, but **adapt recommendations to the actual flat Provider-based codebase** rather than forcing the aspirational `lib/src/` + BLoC + GetX + Dio architecture.

---

## Important File References

| Purpose | Path |
|---------|------|
| Backend entry | `backend/app/main.py` |
| Backend config / env | `backend/app/core/config.py` |
| Backend requirements | `backend/requirements.txt` |
| Alembic config | `backend/alembic.ini` |
| Docker Compose (DB + Redis) | `backend/docker-compose.yml` |
| Flutter entry | `syria_offers_app/lib/main.dart` |
| Flutter config (API URL) | `syria_offers_app/lib/config.dart` |
| Flutter analysis / lint | `syria_offers_app/analysis_options.yaml` |
| Flutter pubspec | `syria_offers_app/pubspec.yaml` |
| Backend tests | `tests/conftest.py`, `tests/test_*.py` |
| Project documentation | `Projektdokumentation.md`, `Projektanalyse.md` |
