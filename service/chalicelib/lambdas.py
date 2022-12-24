from chalice import Blueprint
from lumigo_tracer import lumigo_tracer

from .settings import get_settings

lone = Blueprint(__name__)
settings = get_settings()


@lumigo_tracer()
@lone.lambda_function(name="custom-lambda-chalice")
def custom_lambda_function(event, context):
    return {}
