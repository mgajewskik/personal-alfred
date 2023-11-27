import json

import boto3
import telebot
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import LambdaFunctionUrlResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext

from service.settings import get_settings

settings = get_settings()
logger = Logger(service="api", level=settings.LOG_LEVEL)
app = LambdaFunctionUrlResolver()
bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN, threaded=False)
sqs = boto3.client("sqs", region_name=settings.AWS_REGION)
sns = boto3.client("sns", region_name=settings.AWS_REGION)


@app.get("/")
def index():
    # request doesnt have body and this throws an error
    # logger.info(app.current_event.json_body)
    return {"Hello": "World"}


@app.post("/admin")
def admin():
    logger.info(app.current_event.json_body)
    bot.send_message(settings.ADMIN_CHAT_ID, app.current_event.json_body)
    bot.send_message(settings.ADMIN_CHAT_ID, "SNS message received")
    return {"statusCode": 200, "body": "OK"}


@app.post("/send")
def send():
    logger.info(app.current_event.json_body)

    # response = sqs.send_message(
    #     QueueUrl=settings.SQS_QUEUE_URL,
    #     MessageBody=json.dumps(app.current_event.json_body),
    # )

    response = sns.publish(
        TopicArn=settings.SNS_TOPIC_ARN,
        Message=json.dumps(app.current_event.json_body),
        Subject="New message",
    )
    logger.info(response)
    return response


# TODO check what this correlation ID is used for
@logger.inject_lambda_context(correlation_id_path=correlation_paths.LAMBDA_FUNCTION_URL)
def lambda_handler(event: dict, context: LambdaContext):
    logger.debug(event)

    token = event.get("headers", {}).get("authorization", "")
    if token.replace("Bearer ", "") != settings.DUMMY_AUTH_TOKEN:
        return {"statusCode": 401, "body": "Unauthorized"}

    return app.resolve(event, context)
