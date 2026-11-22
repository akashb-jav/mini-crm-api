import os
import tempfile

# Must be set BEFORE importing main, so tests use a throwaway database
os.environ["DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test.db")

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

GOOD = {"name": "Asha", "email": "asha@example.com", "message": "Need a website"}


def test_health():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_create_enquiry():
    r = client.post("/enquiries", json=GOOD)
    assert r.status_code == 201
    assert r.json()["status"] == "new"


def test_get_enquiry():
    created = client.post("/enquiries", json=GOOD).json()
    r = client.get(f"/enquiries/{created['id']}")
    assert r.status_code == 200
    assert r.json()["name"] == "Asha"


def test_missing_field_rejected():
    r = client.post("/enquiries", json={"name": "Asha"})
    assert r.status_code == 422


def test_not_found():
    assert client.get("/enquiries/99999").status_code == 404


def test_update_status():
    created = client.post("/enquiries", json=GOOD).json()
    r = client.patch(
        f"/enquiries/{created['id']}/status", json={"status": "contacted"}
    )
    assert r.status_code == 200
    assert r.json()["status"] == "contacted"
