import boto3
from chalice import AuthResponse, Blueprint
from telebot.types import Update

from .bot import bot
from .settings import get_settings

api = Blueprint(__name__)
s3 = boto3.client("s3")
settings = get_settings()


# TODO try to use only POST here and test this change
@api.route("/bot", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
def bot_handler():
    # dumping to json makes \" ugly formatting
    # bot.send_message(settings.ADMIN_CHAT_ID, api.current_request.json_body)
    bot.process_new_updates([Update.de_json(api.current_request.json_body)])


@api.authorizer()
def dummy_auth(auth_request) -> AuthResponse:
    token = auth_request.token
    if token.replace("Bearer ", "") == settings.DUMMY_AUTH_TOKEN:
        return AuthResponse(routes=["/", "/env", "/buckets"], principal_id="user")
    return AuthResponse(routes=[], principal_id="user")


@api.route("/", authorizer=dummy_auth)
def index():
    return {"chalice": "example"}
