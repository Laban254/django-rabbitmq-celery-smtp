# mailer/tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_email_task(email):
    send_mail(
        'HNG TASK ',
        'Messaging System with RabbitMQ/Celery and Python Application behind Nginx',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

