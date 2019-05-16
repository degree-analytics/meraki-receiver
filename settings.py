# -*- coding: utf-8 -*-
"""Application configuration."""
import os


class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get('SECRET_KEY', 'this is a really fun secret')  # TODO: CHANGE ME

    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = APP_DIR
    LOCAL = False
    TESTING = False
    BCRYPT_LOG_ROUNDS = 13
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    THREADED = True
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    ########## APPLICATION ACCESS SETTINGS ######################################
    AWS_ACCESS_KEY = ""  # TODO: CHANGE ME
    AWS_SECRET_KEY= "" # TODO: CHANGE ME
    AWS_FIREHOSE_DELIVERY_STREAM_NAME = ''  # TODO: CHANGE ME IF APPLICABLE
    API_VERSION = '1.0'
    MERAKI_VALIDATOR = ""  # TODO: CHANGE ME
    MERAKI_SECRET = "" # TODO: CHANGE ME
    MERAKI_API_KEY = "" # TODO: CHANGE ME
    MERAKI_ORGANIZATION_ID = "" # TODO: CHANGE ME
    MERAKI_NETWORK_ID = ""
    LOG_FILENAME = "log"


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'PROD'
    DEBUG = False


class DevConfig(ProdConfig):
    """Development configuration."""

    ENV = 'DEV'


class LocalConfig(Config):
    """Local configuration."""

    ENV = 'LOCAL'
    DEBUG = True
    LOCAL = True
    DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = False  # Don't bundle/minify static assets
