import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
# this is also used in manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
#os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = Celery('celery_jobs')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.broker_url = 'redis://localhost:6379/5'
app.conf.result_backend = 'redis://localhost:6379/6'