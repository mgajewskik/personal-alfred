from chalice import Blueprint
from lumigo_tracer import lumigo_tracer

from .settings import APISettings


def get_lambdas(settings: APISettings) -> Blueprint:

    lb = Blueprint(__name__)

    @lumigo_tracer()
    @lb.lambda_function(name="custom-lambda-chalice")
    def custom_lambda_function(event, context):
        return {}

    return lb
