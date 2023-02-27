# Arzion Backend Boilerplate

This is a backend boilerplate based on many project we did in the past.
It is based on the following technologies:

- Flask
- SqlAlchemy


## Instance configuration file

You must create a this file
`instance/config.py`

```python

ENV = "development"
SQLALCHEMY_DATABASE_URI = "postgresql://restapi:restapi@db:5432/restapi"
SECRET_KEY = "PLEASE_REPLACE_THIS"
DISCORD_WEBHOOK_URL = "PLEASE_REPLACE_THIS"

SYSLOG_HOST = "logs3.papertrailapp.com"
SYSLOG_PORT = 32030

REDIS_URL = "redis://redis:6379/0"

CELERY_CONFIG = {
    "broker_url": REDIS_URL,
    "result_backend_url": REDIS_URL,
    "accept_content": ["json"],
    "task_serializer": "json",
    "redis_max_connections": 5,
}

# RedisCache
CACHE_REDIS_URL = REDIS_URL

# FilesystemCache
CACHE_DIR = "/tmp/cache/"



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
