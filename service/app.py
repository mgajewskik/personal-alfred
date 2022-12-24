import os

from chalice.app import Chalice, LambdaFunctionEvent

# HACK: imports in lambda are different than local
if os.environ.get("SOURCE") == "lambda":
    from chalicelib.api import get_api
    from chalicelib.bot import get_bot
    from chalicelib.events import get_events
    from chalicelib.lambdas import get_lambdas
    from chalicelib.settings import get_settings
else:
    from service.chalicelib.api import get_api
    from service.chalicelib.bot import get_bot
    from service.chalicelib.events import get_events
    from service.chalicelib.lambdas import get_lambdas
    from service.chalicelib.settings import get_settings

settings = get_settings()
bot = get_bot(settings)


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

    return app


app = create_app()
