from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'send_message.settings')


# run worker: celery -A send_message worker -l info
app = Celery('send_message')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

#for run: celery -A send_message beat -l info
app.conf.beat_schedule = {                       # Defining pending tasks
    'send-email-every-day': {
        'task': 'main.tasks.send_subs_email',
        'schedule': crontab(minute=0, hour='9, 21')
    }
}