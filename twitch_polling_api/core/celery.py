from celery import Celery

from twitch_polling_api.core.config import settings

app = Celery('twitch_polling_api', broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)
task_modules = ['twitch_polling_api.core', 'twitch_polling_api.polls', 'twitch_polling_api.users']
app.autodiscover_tasks(task_modules)
