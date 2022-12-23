import os

from chalice.app import Chalice, LambdaFunctionEvent

# HACK: imports in lambda are different than local
if os.environ.get("SOURCE") == "lambda":
    from chalicelib.api import api
    from chalicelib.events import event
    from chalicelib.lambdas import lone
    from chalicelib.settings import get_settings
else:
    from service.chalicelib.api import api
    from service.chalicelib.events import event
    from service.chalicelib.lambdas import lone
    from service.chalicelib.settings import get_settings


def create_app():
    settings = get_settings()
    app = Chalice(app_name="alfred")
    app.log.setLevel(settings.LOG_LEVEL)
    app.register_blueprint(api)
    app.register_blueprint(lone)
    app.register_blueprint(event)

    @app.middleware("all")
    def log_event(event, get_response):
        # TODO authorization is showing as a plain text in debug log
        if isinstance(event, LambdaFunctionEvent):
            app.log.info(event.context)
        else:
            app.log.info(event.json_body)
        app.log.debug(event.to_dict())
        return get_response(event)

    return app


app = create_app()
