from typing import Generator
from unittest.mock import patch

import boto3
import pytest
from chalice.test import Client
from moto.s3 import mock_s3
from telebot import TeleBot, apihelper, util

from service.chalicelib.settings import APISettings


# making this a fixture doesn't make sense because it is never called and
# therefore does not return the class instance
def test_api_settings() -> APISettings:
    return APISettings(
        LOG_LEVEL="DEBUG",
        DOMAIN_NAME="example.com",
        CERTIFICATE_ARN="arn:aws:acm:us-east-1:123456789012:certificate/12345678-1234-1234-1234-123456789012",
        S3_BUCKET_NAME="example-bucket",
        USERS_TABLE_STREAM_ARN="arn:aws:dynamodb:us-east-1:123456789012:table/example-table/stream/2015-06-27T00:48:05.899",
        ADMIN_CHAT_ID=123456789,
        DUMMY_AUTH_TOKEN="cewd",
        TELEGRAM_BOT_TOKEN="123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
    )


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


@pytest.fixture(scope="session")
def s3_mock():
    with mock_s3():
        yield boto3.client("s3", region_name="us-east-1")


@pytest.fixture(scope="session")
def test_bucket(s3_mock) -> str:
    bucket_name = "test_bucket_name"
    s3_mock.create_bucket(Bucket=bucket_name)
    return bucket_name


# TODO evaluate this further, mocker does not seem like useful here if I can
# mock all clients with moto
@pytest.fixture()
def client_mocks(mocker, s3_mock):
    # mocker.patch(
    #     "service.chalicelib.settings.get_settings", return_value=test_api_settings
    # )
    mocker.patch("service.chalicelib.api.s3", return_value=s3_mock)


# TODO refactor this test bot to make it work properly
# @pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
def test_client() -> Generator[Client, None, None]:

    with patch("service.chalicelib.settings.get_settings") as mock_settings:
        mock_settings.return_value = test_api_settings()

        # TODO look for another patching solution - is it even being used?
        with patch("service.chalicelib.bot.bot") as mock_bot:
            mock_bot.return_value = test_bot_client()

            from service.app import create_app

            app = create_app()
            with Client(app) as client:
                yield client
