import json

import telebot
from aws_lambda_powertools import Logger
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext
from telebot.types import Message, Update

from service.db import Dynamo
from service.models import User
from service.settings import get_settings

settings = get_settings()
logger = Logger(service="bot", level=settings.LOG_LEVEL)
bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN, threaded=False)
db = Dynamo(settings)


@bot.message_handler(commands=["start", "hello"])
def send_welcome(message: Message):

    if not db.add_user(User.from_telegram(message)):
        logger.info("User already exists or request failed")
        bot.send_message(message.chat.id, "Something went wrong")

    bot.send_message(message.chat.id, "Hello, how are you doing?")

    user = db.get_user(message.from_user.id)
    bot.send_message(message.chat.id, str(user.dict()))


@bot.message_handler(func=lambda msg: True)
def echo_all(message: Message):
    bot.send_message(message.chat.id, message.text)


@logger.inject_lambda_context(correlation_id_path=correlation_paths.LAMBDA_FUNCTION_URL)
def lambda_handler(event, context: LambdaContext):
    logger.debug(event)

    try:
        message = json.loads(event.get("body", "{}"))
        bot.process_new_updates([Update.de_json(message)])
        return {"statusCode": 200, "body": "OK"}
    except Exception as e:
        logger.exception(e)
        return {"statusCode": 500, "body": "error"}
