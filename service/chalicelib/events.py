from chalice import Blueprint

from .settings import get_settings

event = Blueprint(__name__)
settings = get_settings()


# @event.on_dynamodb_record(stream_arn=settings.USERS_TABLE_STREAM_ARN)
# def handle_ddb_message(event):
#     for record in event:
#         event.log.debug("New: %s", record.new_image)
