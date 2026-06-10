from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import apply_rate_limiting


def test_global_rate_limit_100_requests_per_minute_is_enforced():
    app = FastAPI()
    apply_rate_limiting(app)

    @app.get("/ping")
    async def ping():
        return {"ok": True}

    with TestClient(app) as client:
        for _ in range(100):
            response = client.get("/ping")
            assert response.status_code == 200

        blocked = client.get("/ping")
        assert blocked.status_code == 429
