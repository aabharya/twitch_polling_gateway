import logging

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from root.celery import app as celery_app
from users.models import User

logger = logging.getLogger('user_management:signals')


@receiver(post_save, sender=User)
def dispatch_user_creation_event(sender, instance: User, created, **kwargs) -> None:
    if not created or not instance:
        return
    gateway_user_context = {
        'username': instance.username,
        'email': instance.email,
        'first_name': instance.first_name,
        'last_name': instance.last_name,
        'public_id': instance.public_id,
    }
    for consumer_queue in settings.GATEWAY_CONSUMERS:
        celery_app.send_task('create_user_from_gateway', kwargs=gateway_user_context, queue=consumer_queue)
    log_message = '"User Management Gateway": Dispatched user creation event for username: #{}'
    logger.info(log_message.format(instance.username))
