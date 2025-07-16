import logging

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from root.celery import app as celery_app
from users.models import User

logger = logging.getLogger('user_management:signals')


@receiver(post_save, sender=User)
def dispatch_user_creation_event(sender, instance: User, created, **kwargs) -> None:
    task_name = (settings.GATEWAY_USER_CREATE_TASK_NAME if created else settings.GATEWAY_USER_UPDATE_TASK_NAME).lower()
    gateway_user_context = {
        'created_at': instance.created_at.isoformat(),
        'updated_at': instance.updated_at.isoformat(),
        'username': instance.username,
        'email': instance.email,
        'first_name': instance.first_name,
        'last_name': instance.last_name,
        'public_id': instance.public_id,
    }
    for consumer_queue in settings.GATEWAY_CONSUMERS:
        celery_app.send_task(task_name, kwargs=gateway_user_context, queue=consumer_queue)
    log_message = '"User Management Gateway": Dispatched user event `{}` for username: #{}'
    logger.info(log_message.format(task_name, instance.username))
