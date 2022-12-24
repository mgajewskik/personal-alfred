import json


def test_bot_handler(test_client, test_bot_event):
    response = test_client.http.post(
        "/bot",
        headers={"Content-Type": "application/json"},
        body=json.dumps(test_bot_event),
    )

    assert response.json_body is None
    assert response.status_code == 200


def test_index(test_client):
    response = test_client.http.get("/", headers={"authorization": "cewd"})
    assert response.json_body == {"chalice": "example"}
