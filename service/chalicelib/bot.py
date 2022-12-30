from typing import Optional

import telebot

from .db import Dynamo
from .models import User
from .protocols import Bot
from .settings import APISettings


def get_bot(settings: APISettings, db: Dynamo) -> Bot:
    bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN, threaded=False)

    @bot.message_handler(commands=["start", "hello"])
    def send_welcome(message: telebot.types.Message):

        if not db.add_user(User.from_telegram(message)):
            # TODO create a proper logger
            print("User already exists or request failed")
            bot.send_message(message.chat.id, "Something went wrong")

        bot.send_message(message.chat.id, "Hello, how are you doing?")

        user = db.get_user(message.from_user.id)
        bot.send_message(message.chat.id, str(user.dict()))

    @bot.message_handler(func=lambda msg: True)
    def echo_all(message: telebot.types.Message):
        bot.send_message(message.chat.id, message.text)

    return bot


# TODO create light bot for places where we don't want to handle all commands
# but just sent admin messages
