from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging_system.settings')

app = Celery('tasks_app')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
