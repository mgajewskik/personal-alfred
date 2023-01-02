from .models import BotEvent


def get_bot_event(context) -> BotEvent:
    return BotEvent(**context.current_request.json_body)
