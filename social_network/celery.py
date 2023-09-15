from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network.settings')
app = Celery('social_network', broker='redis://localhost/', backend='redis://localhost/')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

'''
NOTE: Personal notes in running celery
Celery is a python package that is linked to the enviroment

Start celery with:
- celery --app=social_network.celery:app worker --loglevel=INFO --pidfile=celery.pid
'''