import json


def test_bot_lambda_handler(test_bot, test_bot_event, lambda_context):
    minimal_event = {
        "rawPath": "/",
        "requestContext": {
            "requestContext": {
                "requestId": "227b78aa-779d-47d4-a48e-ce62120393b8"
            },  # correlation ID
            "http": {
                "method": "POST",
            },
            "stage": "$default",
        },
        "body": json.dumps(test_bot_event),
    }

    ret = test_bot(minimal_event, lambda_context)
    # TODO fix bot client to have this method and act like a proper test client
    # AttributeError: 'function' object has no attribute 'process_new_updates'"
    assert ret["statusCode"] == 500
