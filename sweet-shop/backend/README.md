# Backend - Sweet Shop API

Requirements
- Python 3.10+
- MongoDB (see docker-compose.yml in repo root)

Setup
1. Copy `.env.example` to `.env` and configure values (JWT secret, admin secret, MONGO_URI).
2. Start MongoDB with Docker:

```powershell
docker-compose up -d
```

3. Install dependencies:

```powershell
cd backend
pip install -r requirements.txt
```

Run app

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Run tests

```powershell
cd backend
pytest -q
```

Notes
- Tests expect a running MongoDB instance; the `docker-compose.yml` in the project root defines a `mongo` service.

- **Dependency pin:** `pydantic` is pinned to `<2.10` in `requirements.txt` because `BaseSettings` was moved to `pydantic-settings` in `pydantic` 2.10+, which causes an import error in this project. If you see a `PydanticImportError`, run `pip install -r requirements.txt` to install the pinned version.
