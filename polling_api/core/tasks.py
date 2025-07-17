from polling_api.core.celery import app
from polling_api.core.config import settings


@app.task(name='dummy_task', ignore_result=False, queue=settings.CELERY_QUEUE_NAME)
def dummy_task(x, y):
    return x + y
