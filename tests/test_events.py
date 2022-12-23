# TODO prepare mock dynamodb stream event
# def test_dynamo_message(test_client):
#     result = test_client.lambda_.invoke(
#         "handle_ddb_message",
#         {"Records": [{"NewImage": {"id": {"S": "1"}}, "dynamodb": "test"}]},
#     )
#     assert result.payload == {}
