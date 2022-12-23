import telebot

from .settings import get_settings

settings = get_settings()

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN, threaded=False)

# TODO fill in the handlers here


@bot.message_handler(commands=["start", "hello"])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.send_message(message.chat.id, message.text)