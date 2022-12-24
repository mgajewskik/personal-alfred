from chalice import AuthResponse, Blueprint
from telebot.types import Update

from .protocols import Bot
from .settings import APISettings


def get_api(bot: Bot, settings: APISettings) -> Blueprint:
    api = Blueprint(__name__)

    @api.route("/bot", methods=["POST"])
    def bot_handler():
        # dumping to json makes \" ugly formatting
        # bot.send_message(settings.ADMIN_CHAT_ID, api.current_request.json_body)
        bot.process_new_updates([Update.de_json(api.current_request.json_body)])

    @api.authorizer()
    def dummy_auth(auth_request) -> AuthResponse:
        token = auth_request.token
        if token.replace("Bearer ", "") == settings.DUMMY_AUTH_TOKEN:
            return AuthResponse(routes=["/"], principal_id="user")
        return AuthResponse(routes=[], principal_id="user")

    @api.route("/", authorizer=dummy_auth)
    def index():
        return {"chalice": "example"}

    return api
