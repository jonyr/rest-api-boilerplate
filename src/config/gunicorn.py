# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
# import multiprocessing
# import os

# from src.project.helpers import strtobool

# bind = "0.0.0.0:8000"

# accesslog = None
# access_log_format = "%(h)s %(l)s %(u)s %(t)s '%(r)s' %(s)s %(b)s '%(f)s' '%(a)s' in %(D)sµs"  # noqa: E501

# errorlog = "-"
# loglevel = "ERROR"

# workers = int(multiprocessing.cpu_count() * 2)
# threads = 1

# reload = True

import multiprocessing

# workers = int(multiprocessing.cpu_count() * 2)

access_log_format = "%(h)s %(l)s %(u)s %(t)s '%(r)s' %(s)s %(b)s '%(f)s' '%(a)s' in %(D)sµs"  # noqa: E501
errorlog = None
accesslog = None
