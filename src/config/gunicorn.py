# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
import multiprocessing
import os

from src.project.helpers import strtobool

bind = f'0.0.0.0:{os.getenv("GUNICORN_PORT", "8000")}'

accesslog = None
access_log_format = "%(h)s %(l)s %(u)s %(t)s '%(r)s' %(s)s %(b)s '%(f)s' '%(a)s' in %(D)sµs"  # noqa: E501

errorlog = "-"
loglevel = f'{os.getenv("GUNICORN_ERROR_LOG_LEVEL", "ERROR")}'

workers = int(os.getenv("WEB_CONCURRENCY", multiprocessing.cpu_count() * 2))
threads = int(os.getenv("PYTHON_MAX_THREADS", "1"))

reload = bool(strtobool(os.getenv("WEB_RELOAD", "false")))
