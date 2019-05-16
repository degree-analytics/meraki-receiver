# Libraries
import logging
import logging.handlers

from flask import Flask
import os
from settings import Config, DevConfig, ProdConfig, LocalConfig

version = "2.0"


def create_app(config_object=None):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """

    app = Flask(__name__)
    app.config.from_object(get_config(config_object))
    cache_logger(get_logger())
    register_blueprints(app)
    register_health_endpoint(app)

    return app


LOGGER = None


def cache_logger(logger):
    global LOGGER
    LOGGER = logger


def get_logger():
    if LOGGER:
        return LOGGER

    logger = logging.getLogger('MyLogger')
    log_file = Config.LOG_FILENAME
    handler = logging.handlers.TimedRotatingFileHandler(log_file, backupCount=7 * 24)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger


def get_config(config=None):
    if config is not None and issubclass(config, Config):
        return config
    config = config or os.getenv("SERVER_TYPE")

    out = LocalConfig

    if config == "PROD":
        out = ProdConfig
    if config == "DEV":
        out = DevConfig

    return out


def register_health_endpoint(app):
    @app.route("/")
    def hello():
        return 'hello :)'


def register_blueprints(app):
    """Register Flask blueprints."""
    from api_dir.meraki_receiver import mod as meraki_reciever_mod

    app.register_blueprint(meraki_reciever_mod)
