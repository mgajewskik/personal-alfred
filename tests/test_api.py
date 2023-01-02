# def test_bot_handler(test_client, test_bot_event):
#     response = test_client.http.post(
#         "/bot",
#         headers={"Content-Type": "application/json"},
#         body=json.dumps(test_bot_event),
#     )
#
#     assert response.json_body is None
#     assert response.status_code == 200
#
#
# def test_index(test_client):
#     response = test_client.http.get("/", headers={"authorization": "cewd"})
#     assert response.json_body == {"chalice": "example"}


def test_api_lambda_handler(test_api, lambda_context):
    minimal_event = {
        "rawPath": "/",
        "headers": {"authorization": "cewd"},
        "requestContext": {
            "requestContext": {
                "requestId": "227b78aa-779d-47d4-a48e-ce62120393b8"
            },  # correlation ID
            "http": {
                "method": "GET",
            },
            "stage": "$default",
        },
        "body": '{"test": "test"}',
    }

    ret = test_api(minimal_event, lambda_context)
    # apparently doesn't return a model
    # TODO wrap this in a test handler in conftest
    # {'statusCode': 200, 'body': '{"Hello":"World"}', 'isBase64Encoded': False, 'headers': {'Content-Type': 'application/json'}, 'cookies': []}
    assert ret["statusCode"] == 200
    assert ret["body"] == '{"Hello":"World"}'
