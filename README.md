# Arzion Backend Boilerplate

This is a backend boilerplate based on many project we did in the past.
It is based on the following technologies:

- [Flask](https://flask.palletsprojects.com/en/2.2.x/)
- [SqlAlchemy](https://www.sqlalchemy.org)
- [Marshmallow](https://marshmallow.readthedocs.io/en/stable/)
- [Celery](https://docs.celeryq.dev/en/stable/)
- [JWT](https://flask-jwt-extended.readthedocs.io/en/stable/)
- [CORS](https://flask-cors.corydolphin.com/en/latest/configuration.html)

## Instance configuration file

You must create a this file
`instance/config.py`

```python

ENV = "development"

SECRET_KEY = "PLEASE_REPLACE_THIS"
SECRET_KEY = "PLEASE_REPLACE_THIS"

SQLALCHEMY_DATABASE_URI = "postgresql://{user}:{password}@{host}:{port}/{dbnmame}"

DISCORD_WEBHOOK_URL = "PLEASE_REPLACE_THIS"

SYSLOG_HOST = "logs3.papertrailapp.com"
SYSLOG_PORT = 32030

REDIS_URL = "redis://{host}:{port}/{dbname}"

CELERY_CONFIG = {
    "broker_url": REDIS_URL,
    "result_backend_url": REDIS_URL,
    "accept_content": ["json"],
    "task_serializer": "json",
    "redis_max_connections": 5,
}

# FilesystemCache
CACHE_DIR = "/tmp/cache/"

# RedisCache
CACHE_REDIS_URL = REDIS_URL

# MemcachedCache
CACHE_MEMCACHED_SERVERS = ["{host}:{port}"]

# AWS Account
AWS_DEFAULT_REGION = "PLEASE_REPLACE_THIS"
AWS_ACCESS_KEY_ID = "PLEASE_REPLACE_THIS"
AWS_SECRET_ACCESS_KEY = "PLEASE_REPLACE_THIS"

# https://console.cloud.google.com/apis/credentials/key/9c6a62f4-00ef-4a38-b3da-70935d76dd8a?hl=es&project=arzionsrl
GOOGLE_MAPS_API_KEY = "PLEASE_REPLACE_THIS"

# https://flask-cors.corydolphin.com/en/latest/configuration.html
CORS = ["*"]

```
## Running with Docker the whole stack

The whole stack include two aditional containers for Postgres and Redis. If you have your own Postgres and Redis just follow the steps described in the next section.

Before we start the containers create this file

`/instance/.env`

```bash
#!/bin/sh

ENV=development

# Redis
REDIS_DATA=./services/redis/data

# Postgres
POSTGRES_PORT=5432
POSTGRES_DATA=./services/postgres/data
POSTGRES_BACKUPS=./services/postgres/backups
POSTGRES_USER=restapi
POSTGRES_PASSWORD=restapi
POSTGRES_DB=restapi

# Api Core
FLASK_API_PORT=8000

# Flower
FLOWER_PORT=5555
```

### Start

```bash
./manager.sh fullstack
```

### Stop
```bash
./manager.sh fullstop
```

## Internationalization

The project has a dependency with [Flask Babel](https://python-babel.github.io/flask-babel/)

# Third Party Libraries

Datetimes manipulation with [Pendulum](https://pendulum.eustace.io/docs/). See all the valid formatters [here](https://pendulum.eustace.io/docs/#formatter)
