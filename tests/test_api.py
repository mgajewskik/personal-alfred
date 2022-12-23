import json


def test_bot_handler(test_client, test_bot_event):
    # TODO check why no other methods are allowed here
    response = test_client.http.get(
        "/bot",
        headers={"Content-Type": "application/json"},
        body=json.dumps(test_bot_event),
    )

    assert response.json_body is None
    assert response.status_code == 200


def test_index(test_client):
    response = test_client.http.get("/")
    assert response.json_body == {"chalice": "example"}


# def test_buckets(test_client, test_bucket):
#     response = test_client.http.get("/buckets")
#     assert response.json_body == {"buckets": []}
#
#
# # TODO check why authorization is not working in tests
# def test_env(test_client):
#     # response = test_client.http.get("/env", headers={"Authorization": "cewd"})
#     response = test_client.http.get("/env")
#     assert response.json_body == {"env": {"DOMAIN_NAME": "example.com"}}
