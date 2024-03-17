import pytest
from fastapi.testclient import TestClient
from fastapi import status
from model.user import User
from main import app

client = TestClient(app)


@pytest.fixture
def sample() -> User:
    return User(name="sana", hash="Winners5")


def test_create(sample):
    resp = client.post("/user", json=sample.model_dump())
    assert resp.status_code == status.HTTP_201_CREATED


def test_create_duplicate(sample):
    resp = client.post("/user", json=sample.model_dump())
    assert resp.status_code == status.HTTP_409_CONFLICT


def test_get_one(sample):
    resp = client.get(f"/user/{sample.name}")
    assert resp.json() == sample.model_dump()


def test_get_one_missing():
    resp = client.get("/user/bobcat")
    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_modify(sample):
    resp = client.patch(f"/user/{sample.name}", json=sample.model_dump())
    assert resp.json() == sample.model_dump()


def test_modify_missing(sample):
    resp = client.patch("/user/dumbledore", json=sample.model_dump())
    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_delete(sample):
    resp = client.delete(f"/user/{sample.name}")
    assert resp.json() is None
    assert resp.status_code == status.HTTP_200_OK


def test_delete_missing(sample):
    resp = client.delete(f"/user/{sample.name}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
