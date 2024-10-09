from celery import Celery


class Settings:
    SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:5571@localhost:5433/new_db"


settings = Settings()

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

celery = Celery("tasks",
                broker=CELERY_BROKER_URL,
                backend=CELERY_RESULT_BACKEND,
                include=["tasks"])


celery.conf.update(
    enable_utc=True,
    timezone='UTC',
    beat_schedule={
        'fetch_stocks_every_minute': {
            'task': 'tasks.fetch_all_stocks',
            'schedule': 10.0,  # Run every 60 seconds
        },
    }
)

