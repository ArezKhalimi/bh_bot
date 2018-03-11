from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.concurrency import asynpool
from celery.schedules import crontab

from django.conf import settings

CELERY_TIMEZONE = 'Europe/Kiev'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitbot.settings')

app = Celery('fitbot')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

asynpool.PROC_ALIVE_TIMEOUT = 10

