from celery import Celery

from polling_api.core.config import settings

app = Celery('polling_api', broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)
task_modules = ['polling_api.core', 'polling_api.polls', 'polling_api.users']
app.autodiscover_tasks(task_modules)
