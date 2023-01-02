from dataclasses import dataclass
from unittest.mock import patch

import boto3
import pytest
from moto.s3 import mock_s3
from telebot import TeleBot, apihelper, util

from service.settings import APISettings


def mock_api_settings() -> APISettings:
    return APISettings(
        LOG_LEVEL="DEBUG",
        # S3_BUCKET_NAME="example-bucket",
        DYNAMO_TABLE_NAME="example-table",
        DYNAMO_TABLE_STREAM_ARN="arn:aws:dynamodb:us-east-1:123456789012:table/example-table/stream/2015-06-27T00:48:05.899",
        ADMIN_CHAT_ID=123456789,
        DUMMY_AUTH_TOKEN="cewd",
        TELEGRAM_BOT_TOKEN="123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
    )


@pytest.fixture(scope="session")
def settings_mock() -> None:
    with patch("service.settings.get_settings", new=mock_api_settings):
        yield


@pytest.fixture(scope="session")
def bot_mock() -> None:
    with patch("service.lambdas.bot.bot", new=test_bot_client):
        yield


@pytest.fixture(scope="session")
def test_api(settings_mock):
    from service.lambdas.api import lambda_handler

    yield lambda_handler


@pytest.fixture(scope="session")
def test_bot(settings_mock, bot_mock):
    from service.lambdas.bot import lambda_handler

    yield lambda_handler


@pytest.fixture(scope="session")
def test_bot_event():
    return {
        "update_id": 123456789,
        "message": {
            "message_id": 44,
            "from": {
                "id": 123456789,
                "is_bot": False,
                "first_name": "test_name",
                "username": "test_name",
                "language_code": "en",
            },
            "chat": {
                "id": 123456789,
                "first_name": "test_name",
                "username": "test_name",
                "type": "private",
            },
            "date": 1671788689,
            "text": "test",
        },
    }


# TODO refactor this test bot to make it work properly
@pytest.fixture(scope="session")
def test_bot_client():
    def custom_sender(method, url, **kwargs):
        print(
            "custom_sender. method: {}, url: {}, params: {}".format(
                method, url, kwargs.get("params")
            )
        )
        result = util.CustomRequestResponse(
            '{"ok":true,"result":{"message_id": 1, "date": 1, "chat": {"id": 1, "type": "private"}}}'
        )
        return result

    # this bot will not have any methods inherited from the real bot - useless
    apihelper.CUSTOM_REQUEST_SENDER = custom_sender
    return TeleBot("test")
    # res = tb.send_message(123, "Test")


@pytest.fixture
def lambda_context():
    @dataclass
    class LambdaContext:
        function_name: str = "test"
        memory_limit_in_mb: int = 128
        invoked_function_arn: str = (
            "arn:aws:lambda:eu-west-1:123456789012:function:test"
        )
        aws_request_id: str = "da658bd3-2d6f-4e7b-8ec2-937234644fdc"

    return LambdaContext()


@pytest.fixture(scope="session")
def s3_mock():
    with mock_s3():
        yield boto3.client("s3", region_name="us-east-1")


@pytest.fixture(scope="session")
def test_bucket(s3_mock) -> str:
    bucket_name = "test_bucket_name"
    s3_mock.create_bucket(Bucket=bucket_name)
    return bucket_name
