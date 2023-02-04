class DefaultConfig:

    ENV = "production"
    JSON_SORT_KEYS = True
    CELERY_CONFIG = {
        "broker_url": "redis://192.168.1.5:6379/0",
        "result_backend_url": "redis://192.168.1.5:6379/0",
    }
