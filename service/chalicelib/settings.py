from pydantic import BaseSettings


class APISettings(BaseSettings):
    # LOG_LEVEL: str = "INFO"
    LOG_LEVEL: str = "DEBUG"
    AWS_REGION: str = "eu-west-1"

    DOMAIN_NAME: str
    CERTIFICATE_ARN: str
    S3_BUCKET_NAME: str
    USERS_TABLE_NAME: str
    USERS_TABLE_STREAM_ARN: str

    ADMIN_CHAT_ID: int
    DUMMY_AUTH_TOKEN: str
    TELEGRAM_BOT_TOKEN: str


def get_settings():
    return APISettings()
