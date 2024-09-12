from src.endpoints.tasks import *
from src.endpoints.users import *
from main import *
from fastapi.testclient import TestClient
from dotenv import dotenv_values
from bson import ObjectId, json_util
from jose import jwt
import pytest, time, json
from mongoengine import connect, disconnect

config = dotenv_values(".env")
client = TestClient(app)

# def test_home():
#     response = client.get("/Tasks")
#     assert response.status_code == 200
#     assert response.json() == None
@pytest.fixture
def db_conn():
        disconnect()
        connect('mongoenginetest', host='mongomock://localhost/mocking_db')

@pytest.fixture
def jwt_token():
    # Create a sample valid JWT token
    payload = json.loads(json_util.dumps({"exp": time.time() + 1000, "_id": ObjectId('66ccafdd30a846b4e0d8f5b3')}))
    token = jwt.encode(payload, config["JWT_SECRET_KEY"], config["ALGORITHM"])
    return token

def test_list_tasks(jwt_token,db_conn):
    response = client.get("/Tasks/", headers={"Accept": "application/json", "Authorization": f"Bearer {jwt_token}"}, json={"limit": 2})

    assert response.status_code == 201    

def test_create_item(jwt_token,db_conn):
    response = client.post(
        "/Tasks/", headers={"Accept": "application/json", "Authorization": f"Bearer {jwt_token}"},
        json={ "title": "Foo Bar", "description": "The Foo Barters"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "title": "Foo Bar",
        "description": "The Foo Barters",
    }


def test_list_tasks_id(jwt_token,db_conn):
    response = client.get("/Tasks/66ccb02c30a846b4e0d8f5b5/", headers={"Accept": "application/json", "Authorization": f"Bearer {jwt_token}"})
    assert response.status_code == 201    

"""
from fastapi.testclient import TestClient
from src.endpoints.tasks import router
from fastapi import APIRouter, Request, status,HTTPException,Depends

client = TestClient(router)


def test_list_task():
    response = client.get("/Tasks/66ccb02c30a846b4e0d8f5b5/")
    assert response.status_code == 200
    assert response.json() == {
        "title": "demo",
        "description": "this is demo",
    }

def test_create_item():
    response = client.post(
        "/",
        json={ "title": "Foo Bar", "description": "The Foo Barters"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Barters",
    }

def test_read_item_bad_token():
    response = client.get("/items/foo", headers={"X-Token": "hailhydra"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_read_nonexistent_item():
    response = client.get("/items/baz", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Barters",
    }


def test_create_item_bad_token():
    response = client.post(
        "/items/",
        headers={"X-Token": "hailhydra"},
        json={"id": "bazz", "title": "Bazz", "description": "Drop the bazz"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_create_existing_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={
            "id": "foo",
            "title": "The Foo ID Stealers",
            "description": "There goes my stealer",
        },
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Item already exists"}

    """