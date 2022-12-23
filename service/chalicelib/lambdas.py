from chalice import Blueprint

from .settings import get_settings

lone = Blueprint(__name__)
settings = get_settings()


@lone.lambda_function(name="custom-lambda-chalice")
def custom_lambda_function(event, context):
    return {}
