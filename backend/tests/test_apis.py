"""pytest to test api outputs"""
# test_main.py
import pytest
from fastapi.testclient import TestClient
from main import app
from schemas.Conversation import Conversation, ConversationFull


test_document_id = None


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client


def test_get_all_conversations(test_client):
    """tests all conversaiotns GET request"""
    response = test_client.get("/conversations")
    # tests response code
    assert response.status_code == 200

    # test model of each conversation
    conversations = response.json()["data"]
    for convo in conversations:
        assert Conversation(**convo)


def test_post_new_conversation(test_client):
    """tests POST request to create new conversation"""
    test_post_data = {
        "name": "Test Conversation",
        "params": {},
        "tokens": 0
    }

    response = test_client.post("/conversations", json=test_post_data)

    assert response.status_code == 201
    # test response
    global test_document_id

    test_document_id = response.json()["id"]

    assert isinstance(test_document_id, str)


def test_wrong_format_post_conversation_request(test_client):
    """tests POST request on wrong format"""

    test_wrong_format = {
        "name": 101,
        "params": {},
        "tokens": 0
    }

    response = test_client.post(
        "/conversations", json=test_wrong_format)

    assert response.status_code == 400

    response = response.json()

    code, message = response["code"], response["message"]

    assert code == 400

    assert message == "Invalid Parameters Provided"


def test_put_request(test_client):
    """tests PUT request to update conversation name, params"""
    test_put_data = {
        "name": "hello there",
        "params": {},
    }

    response = test_client.put(
        f"/conversations/{test_document_id}", json=test_put_data)

    assert response.status_code == 204


def test_wrong_format_put_request(test_client):
    """tests PUT request for wrong format"""
    test_wrong_format = {
        "name": 101,
        "params": {},
    }

    response = test_client.put(
        f"/conversations/{test_document_id}", json=test_wrong_format)

    assert response.status_code == 400

    response = response.json()

    code, message = response["code"], response["message"]

    assert code == 400

    assert message == "Invalid Parameters Provided"


def test_query_llm(test_client):
    """tests POST request to create new conversation"""
    test_post_data = {
        "role": "user",
        "content": "Who is lee hsien loong"
    }

    response = test_client.post(
        f"/queries?id={test_document_id}", json=test_post_data)

    assert response.status_code == 201
    # test response
    id_return = response.json()["id"]

    assert isinstance(id_return, str)


def test_wrong_format_query_llm(test_client):
    """tests POST request to create new conversation"""
    test_wrong_format = {
        "role": "not an actual role",
        "content": 0
    }

    response = test_client.post(
        f"/queries?id={test_document_id}", json=test_wrong_format)

    assert response.status_code == 400

    response = response.json()

    code, message = response["code"], response["message"]

    assert code == 400

    assert message == "Invalid Parameters Provided"


def test_get_full_conversations(test_client):
    """tests all conversaiotns GET request"""
    response = test_client.get(f"/conversations/{test_document_id}")
    # tests response code
    assert response.status_code == 200

    # test model of each conversation
    conversation = response.json()
    assert ConversationFull(**conversation)


def test_delete_conversation(test_client):
    """tests DELETE request"""
    response = test_client.delete(f"/conversations/{test_document_id}")
    assert response.status_code == 204
