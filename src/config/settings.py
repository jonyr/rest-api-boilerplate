"""Settings module."""

import os
import logging
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class DefaultConfig:
    """
    Default Configuration
    """

    ENV = "production"

    # JWT Extended
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
    JWT_ERROR_MESSAGE_KEY = "description"

    # BABEL
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"
    BABEL_TRANSLATION_DIRECTORIES = os.path.join(basedir, "../../translations/")

    # Email Template
    APP_NAME = "RestAPI"
    APP_URL = "https://www.morfi.pro"
    APP_LOGO_URL = "https://d2g9qrpaqp4r7k.cloudfront.net/images/restapi/restapi_logo.png"
    APP_BANNER_URL = "https://d2g9qrpaqp4r7k.cloudfront.net/images/restapi/restapi_email_header.jpg"

    # Other colors examples
    # 0511F2 Blue
    # 488C35 Green
    # 488C35 Yellow
    # 488C35 Red
    # 488C35 Pink

    APP_PRIMARY_COLOR = "#488C35"  # Green

    # https://console.cloud.google.com/apis/credentials/key/9c6a62f4-00ef-4a38-b3da-70935d76dd8a?hl=es&project=arzionsrl
    GOOGLE_MAPS_API_KEY = None

    # Logging stuff
    REQUEST_LOGGER = False
    LOG_LEVEL = logging.INFO
    STREAM_LOG_LEVEL = logging.INFO
    SYSLOG_LOG_LEVEL = logging.ERROR
    SYSLOG_ADDRESS = None

