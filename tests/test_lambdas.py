def test_custom_lambda(test_client):
    result = test_client.lambda_.invoke("custom-lambda-chalice", {"test": "test"})
    assert result.payload == {}
