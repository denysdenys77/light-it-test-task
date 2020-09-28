import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store_project.settings')

app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1')


app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
