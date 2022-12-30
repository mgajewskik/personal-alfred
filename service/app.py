import os

# import boto3
from chalice.app import Chalice, LambdaFunctionEvent

# HACK: imports in lambda are different than local
if os.environ.get("SOURCE") == "lambda":
    from chalicelib.api import get_api
    from chalicelib.bot import get_bot
    # from chalicelib.db import get_dynamodb
    from chalicelib.db import Dynamo
    from chalicelib.events import get_events
    from chalicelib.lambdas import get_lambdas
    from chalicelib.settings import get_settings
else:
    from service.chalicelib.api import get_api
    from service.chalicelib.bot import get_bot
    # from service.chalicelib.db import get_dynamodb
    from service.chalicelib.db import Dynamo
    from service.chalicelib.events import get_events
    from service.chalicelib.lambdas import get_lambdas
    from service.chalicelib.settings import get_settings


# HACK chalice doesn't generate required policies
# def dummy():
#     """
#     Collection of all s3.client() functions.
#     The sole purpose is to force Chalice to generate the right permissions in the policy.
#     Does nothing and returns nothing.
#     https://github.com/aws/chalice/issues/692
#     """
#     s3 = boto3.client("s3")
#     s3.put_object()
#     s3.download_file()
#     s3.get_object()
#     s3.list_objects_v2()
#     s3.get_bucket_location()
#     db = boto3.client("dynamodb")
#     db.get_item()
#     db.put_item()
#     db.update_item()
#     db.delete_item()
#     db.query()
#     db.batch_get_item()
#     db.batch_write_item()


settings = get_settings()
# dynamodb = get_dynamodb(settings)
db = Dynamo(settings)
bot = get_bot(settings, db)
# light_bot = get_bot(settings, light=True)
# if False:
#     dummy()


def create_app() -> Chalice:
    app = Chalice(app_name="alfred")
    app.log.setLevel(settings.LOG_LEVEL)
    app.register_blueprint(get_api(bot, settings))
    app.register_blueprint(get_lambdas(settings))
    app.register_blueprint(get_events(settings))

    @app.middleware("all")
    def log_event(event, get_response):
        # TODO authorization is showing as a plain text in debug log
        if isinstance(event, LambdaFunctionEvent):
            app.log.info(event.context)
        else:
            app.log.info(event.json_body)
        app.log.debug(event.to_dict())
        return get_response(event)

    # @app.middleware("all")
    # def gen_policy(event, get_response):
    #     if False:
    #         dummy()
    #     app.log.info("Policy generated")
    #     return get_response(event)
    #
    # return app


app = create_app()
