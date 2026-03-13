from fastapi.testclient import TestClient

from osnit.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ip_lookup() -> None:
    response = client.post("/api/v1/lookup/ip", json={"ip": "8.8.8.8"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["kind"] == "ip"
    assert payload["indicator"] == "8.8.8.8"


def test_port_scan_localhost() -> None:
    response = client.post(
        "/api/v1/scan/ports",
        json={"host": "127.0.0.1", "ports": [1, 22], "timeout": 0.1},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["host"] == "127.0.0.1"
    assert "open_ports" in payload
    assert "closed_ports" in payload


def test_india_sources() -> None:
    response = client.get("/api/v1/india/sources")
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert len(payload) >= 5
