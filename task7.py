import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_employees(tmp_path, monkeypatch):
    test_file = tmp_path / "employees.json"

    test_file.write_text(
        '[{"name": "Ravi", "salary": 30000}]',
        encoding="utf-8",
    )

    monkeypatch.setattr("src.main.DATA_FILE", test_file)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_employees():
    response = client.get("/employees")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_employee():
    response = client.get("/employees/Ravi")

    assert response.status_code == 200
    assert response.json()["name"] == "Ravi"


def test_employee_not_found():
    response = client.get("/employees/Unknown")

    assert response.status_code == 404


def test_invalid_salary():
    response = client.post(
        "/employees",
        json={"name": "Ravi", "salary": -5},
    )

    assert response.status_code == 422


def test_empty_name():
    response = client.post(
        "/employees",
        json={"name": "   ", "salary": 30000},
    )

    assert response.status_code == 422


def test_create_employee():
    response = client.post(
        "/employees",
        json={"name": "Priya", "salary": 40000},
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Priya"