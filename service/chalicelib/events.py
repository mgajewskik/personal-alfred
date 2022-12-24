from chalice import Blueprint

from .settings import APISettings


def get_events(settings: APISettings) -> Blueprint:

    event = Blueprint(__name__)

    # @event.on_dynamodb_record(stream_arn=settings.USERS_TABLE_STREAM_ARN)
    # def handle_ddb_message(event):
    #     for record in event:
    #         event.log.debug("New: %s", record.new_image)

    return event
