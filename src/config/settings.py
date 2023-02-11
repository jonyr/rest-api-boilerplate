class DefaultConfig:

    ENV = "production"
    JSON_SORT_KEYS = True
    CELERY_CONFIG = {
        "broker_url": "redis://redis:6379/0",
        "result_backend_url": "redis://redis:6379/0",
        "accept_content": ["json"],
        "task_serializer": "json",
        "redis_max_connections": 5,
    }
