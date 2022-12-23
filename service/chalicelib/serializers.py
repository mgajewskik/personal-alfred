from chalice import Blueprint

from .models import BotEvent


def get_bot_event(context: Blueprint) -> BotEvent:
    return BotEvent(**context.current_request.json_body)
