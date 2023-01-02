from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import LambdaFunctionUrlResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext

from service.settings import get_settings

settings = get_settings()
logger = Logger(service="api", level=settings.LOG_LEVEL)
app = LambdaFunctionUrlResolver()


@app.get("/")
def index():
    # request doesnt have body and this throws an error
    # logger.info(app.current_event.json_body)
    return {"Hello": "World"}


# TODO check what this correlation ID is used for
@logger.inject_lambda_context(correlation_id_path=correlation_paths.LAMBDA_FUNCTION_URL)
def lambda_handler(event: dict, context: LambdaContext):
    logger.debug(event)

    token = event.get("headers", {}).get("authorization", "")
    if token.replace("Bearer ", "") != settings.DUMMY_AUTH_TOKEN:
        return {"statusCode": 401, "body": "Unauthorized"}

    return app.resolve(event, context)
