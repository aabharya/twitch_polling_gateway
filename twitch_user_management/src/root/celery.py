from celery import Celery

app = Celery('root')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
